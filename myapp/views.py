# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncMonth
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import os

from .models import Product, HomePage, HomeSlide, Commande
from .forms import CommandeForm

# =================== HOME ===================
def home(request):
    """Page d'accueil avec produits disponibles et slides"""
    home_data = HomePage.objects.first()
    products = Product.objects.filter(quantity__gt=0)  # Produits en stock
    slides = HomeSlide.objects.all()
    return render(request, 'home.html', {
        'home_data': home_data,
        'products': products,
        'slides': slides
    })


# =================== COMMANDE ===================
def commande(request, product_id):
    """
    Crée une commande pour un produit donné.
    Calcul automatique du total et redirige vers confirmation.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = CommandeForm(request.POST)
        quantity = int(request.POST.get('quantity', 1))
        if form.is_valid():
            commande = form.save(commit=False)
            commande.product = product
            commande.quantity = quantity
            commande.total_amount = product.price * quantity
            commande.save()
            messages.success(request, "Commande enregistrée avec succès !")
            return redirect('commande_confirmation', commande.id)
    else:
        form = CommandeForm()

    return render(request, 'commande.html', {
        'product': product,
        'form': form
    })


def commande_confirmation(request, commande_id):
    """Affiche la confirmation de la commande"""
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande_confirmation.html', {'commande': commande})


# =================== GENERATION PDF ===================
def generate_pdf(request, commande_id):
    """Génère un PDF de confirmation pour une commande"""
    commande = get_object_or_404(Commande, id=commande_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="commande_{commande.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Logo
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
    if os.path.exists(logo_path):
        p.drawImage(ImageReader(logo_path), 50, height - 47, width=80, height=25, mask='auto')

    # Titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"Confirmation de Commande - #{commande.id}")

    # Ligne séparation
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(50, height - 60, 550, height - 60)

    # Informations commande
    y_position = height - 100
    details = [
        ("Nom du client", commande.customer_name),
        ("Produit", commande.product.name),
        ("Quantité", str(commande.quantity)),
        ("Adresse de livraison", commande.customer_address),
        ("Méthode de paiement", commande.payment),
        ("Date de commande", commande.created_at.strftime("%d/%m/%Y %H:%M")),
        ("Total", f"{commande.total_amount} €"),
    ]

    for label, value in details:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y_position, f"{label} :")
        p.setFont("Helvetica", 12)
        p.drawString(250, y_position, value)
        y_position -= 25

    # Ligne de fin
    p.line(50, y_position - 10, 550, y_position - 10)

    # Remerciement
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position - 40, "Merci pour votre confiance ! 🚀")

    p.showPage()
    p.save()

    return response


# =================== DASHBOARD ADMIN ===================
def dashboard(request):
    """
    Dashboard avec statistiques et graphique des commandes
    """
    products_count = Product.objects.count()
    orders_pending = Commande.objects.filter(status='pending').count()
    orders_delivered = Commande.objects.filter(status='delivered').count()

    monthly_orders = Commande.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(total=Count('id')).order_by('month')

    context = {
        'products_count': products_count,
        'orders_pending': orders_pending,
        'orders_delivered': orders_delivered,
        'monthly_orders': monthly_orders,
    }
    return render(request, 'admin/dashboard.html', context)
