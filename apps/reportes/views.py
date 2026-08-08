import io
import os
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from apps.socios.models import Socio


def aplicar_filtros_socios(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    ciudad = request.GET.get('ciudad', '').strip()
    recibio_souvenir = request.GET.get('recibio_souvenir', '')
    desde = request.GET.get('desde', '').strip()
    hasta = request.GET.get('hasta', '').strip()
    orden = request.GET.get('orden', 'recientes')

    socios = Socio.objects.select_related('user').all()
    if q:
        socios = socios.filter(
            Q(nombre__icontains=q)
            | Q(apellido__icontains=q)
            | Q(email__icontains=q)
            | Q(telefono__icontains=q)
            | Q(ciudad__icontains=q)
            | Q(direccion__icontains=q)
        )
    if estado:
        socios = socios.filter(estado=estado)
    if ciudad:
        socios = socios.filter(ciudad__icontains=ciudad)
    if desde:
        socios = socios.filter(fecha_ingreso__gte=desde)
    if hasta:
        socios = socios.filter(fecha_ingreso__lte=hasta)
    if recibio_souvenir == 'si':
        socios = socios.filter(recibio_souvenir=True)
    elif recibio_souvenir == 'no':
        socios = socios.filter(recibio_souvenir=False)

    ordenamiento = '-fecha_ingreso' if orden == 'recientes' else 'fecha_ingreso'
    socios = socios.order_by(ordenamiento)

    return socios, {
        'q': q,
        'estado': estado,
        'ciudad': ciudad,
        'recibio_souvenir': recibio_souvenir,
        'desde': desde,
        'hasta': hasta,
        'orden': orden,
    }


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reportes_socios(request):
    socios, filtros = aplicar_filtros_socios(request)

    return render(request, 'reportes/reportes_socios.html', {
        'socios': socios,
        **filtros,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def descargar_reporte_socios(request):
    socios, filtros = aplicar_filtros_socios(request)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = {
        'title': ParagraphStyle(
            name='Title',
            fontSize=14,
            leading=18,
            alignment=0,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#0b3d91'),
        ),
        'subtitle': ParagraphStyle(
            name='Subtitle',
            fontSize=9,
            leading=11,
            alignment=0,
            spaceAfter=4,
            textColor=colors.HexColor('#555555'),
        ),
        'normal': ParagraphStyle(
            name='Normal',
            fontSize=7,
            leading=8.5,
            alignment=0,
        ),
    }

    elements = []
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logoAlmacen.png')
    logo = None
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=28, height=28)
        except Exception:
            logo = None

    header_title = Paragraph(
        'Club Amigos - Reporte de Socios',
        ParagraphStyle(
            name='CenteredTitle',
            fontSize=14,
            leading=18,
            alignment=1,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#0b3d91'),
        ),
    )

    filtros_text = []
    if filtros['q']:
        filtros_text.append(f'Búsqueda: {filtros["q"]}')
    if filtros['estado']:
        filtros_text.append(f'Estado: {filtros["estado"].capitalize()}')
    if filtros['ciudad']:
        filtros_text.append(f'Ciudad: {filtros["ciudad"]}')
    if filtros['desde']:
        filtros_text.append(f'Desde: {filtros["desde"]}')
    if filtros['hasta']:
        filtros_text.append(f'Hasta: {filtros["hasta"]}')
    if filtros['recibio_souvenir']:
        filtros_text.append(f'Recibió souvenir: {filtros["recibio_souvenir"].capitalize()}')
    if filtros['orden']:
        orden_label = 'Más recientes' if filtros['orden'] == 'recientes' else 'Más antiguos'
        filtros_text.append(f'Orden: {orden_label}')

    header_meta = Table(
        [
            [Paragraph('<b>Reporte generado:</b>', styles['normal']), Paragraph(datetime.now().strftime('%d/%m/%Y %H:%M'), styles['normal'])],
            [Paragraph('<b>Reportado por:</b>', styles['normal']), Paragraph(request.user.get_full_name() or request.user.username, styles['normal'])],
        ],
        colWidths=[3.2 * cm, 8.5 * cm],
        hAlign='LEFT',
    )
    header_meta.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    if filtros_text:
        header_filters = Table(
            [[Paragraph('<b>Filtros aplicados:</b>', styles['normal']), Paragraph(' | '.join(filtros_text), styles['normal'])]],
            colWidths=[3.2 * cm, 8.5 * cm],
            hAlign='LEFT',
        )
        header_filters.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
    else:
        header_filters = None

    if logo:
        left_header = [[logo], [Spacer(1, 4)], [header_meta]]
        if header_filters:
            left_header.append([Spacer(1, 2)])
            left_header.append([header_filters])
        left_table = Table(left_header, colWidths=[6.0 * cm])
        left_table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        header_table = Table(
            [[left_table, header_title]],
            colWidths=[6.0 * cm, 10.7 * cm],
            hAlign='LEFT',
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(header_table)
    else:
        elements.append(header_title)
        elements.append(header_meta)
        if header_filters:
            elements.append(Spacer(1, 2))
            elements.append(header_filters)

    elements.append(Spacer(1, 12))

    data = [
        ['N°', 'Socio', 'Correo', 'Teléfono', 'Ciudad', 'Estado', 'Souvenir', 'Ingreso'],
    ]
    for idx, socio in enumerate(socios, 1):
        data.append([
            str(idx),
            f'{socio.nombre} {socio.apellido}',
            socio.email,
            socio.telefono or '-',
            socio.ciudad or '-',
            socio.get_estado_display(),
            'Sí' if socio.recibio_souvenir else 'No',
            socio.fecha_ingreso.strftime('%d/%m/%Y'),
        ])

    table = Table(
        data,
        repeatRows=1,
        hAlign='LEFT',
        colWidths=[0.7 * cm, 3.3 * cm, 4.0 * cm, 2.3 * cm, 1.8 * cm, 1.8 * cm, 1.6 * cm, 1.8 * cm],
    )
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0b3d91')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('ALIGN', (5, 0), (5, -1), 'CENTER'),
        ('ALIGN', (6, 0), (6, -1), 'CENTER'),
        ('ALIGN', (7, 0), (7, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#d9d9d9')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7ff')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 16))
    elements.append(Paragraph('Club Amigos - Unidos por una comunidad más fuerte.', styles['subtitle']))
    doc.build(elements)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='reporte_socios.pdf')
