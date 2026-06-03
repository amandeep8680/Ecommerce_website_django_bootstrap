from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import (
    Product,
    Category,
    Review,
    Wishlist,
    Order,
    OrderItem
)


# HOME PAGE


def home(request):

    featured_products = Product.objects.filter(
        featured=True
    )[:8]

    trending_products = Product.objects.order_by(
        '-rating'
    )[:8]

    new_arrivals = Product.objects.order_by(
        '-created_at'
    )[:8]

    best_sellers = Product.objects.order_by(
        '-stock'
    )[:8]

    products = Product.objects.all()[:12]

    categories = Category.objects.all()

    return render(
        request,
        'home.html',
        {
            'products': products,
            'featured_products': featured_products,
            'trending_products': trending_products,
            'new_arrivals': new_arrivals,
            'best_sellers': best_sellers,
            'categories': categories
        }
    )




# SHOP PAGE

def products(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    query = request.GET.get('q')

    category_id = request.GET.get('category')

    min_price = request.GET.get('min_price')

    max_price = request.GET.get('max_price')

    sort = request.GET.get('sort')

    # SEARCH

    if query:

        products = products.filter(

            Q(name__icontains=query) |

            Q(description__icontains=query) |

            Q(brand__icontains=query)

        )

    # CATEGORY FILTER

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    # PRICE FILTER

    if min_price:

        products = products.filter(
            price__gte=min_price
        )

    if max_price:

        products = products.filter(
            price__lte=max_price
        )

    # SORTING

    if sort == 'price_low':

        products = products.order_by('price')

    elif sort == 'price_high':

        products = products.order_by('-price')

    elif sort == 'rating':

        products = products.order_by('-rating')

    elif sort == 'newest':

        products = products.order_by('-created_at')

    return render(
        request,
        'products.html',
        {
            'products': products,
            'categories': categories
        }
    )



# PRODUCT DETAIL

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews = Review.objects.filter(
        product=product
    )

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'reviews': reviews,
            'related_products': related_products
        }
    )


# CATEGORY PAGE

def category_products(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    products = Product.objects.filter(
        category=category
    )

    categories = Category.objects.all()

    return render(
        request,
        'products.html',
        {
            'products': products,
            'categories': categories,
            'selected_category': category
        }
    )


# REGISTER


from django.contrib.auth.models import User

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:

            if User.objects.filter(username=username).exists():

                return render(
                    request,
                    'register.html',
                    {
                        'error': 'Username already exists'
                    }
                )

            User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            return redirect('login')

        else:

            return render(
                request,
                'register.html',
                {
                    'error': 'Passwords do not match'
                }
            )

    return render(
        request,
        'register.html'
    )


# CART

def add_to_cart(request, product_id):

    cart = request.session.get(
        'cart',
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):

    cart = request.session.get(
        'cart',
        {}
    )

    products = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        products.append(
            {
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            }
        )

    return render(
        request,
        'cart.html',
        {
            'products': products,
            'total': total
        }
    )


# CHECKOUT


from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    products = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.discounted_price * quantity

        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == "POST":

        order = Order.objects.create(

            user=request.user,

            full_name=request.POST.get(
                'full_name'
            ),

            phone=request.POST.get(
                'phone'
            ),

            address=request.POST.get(
                'address'
            ),

            city=request.POST.get(
                'city'
            ),

            state=request.POST.get(
                'state'
            ),

            pincode=request.POST.get(
                'pincode'
            ),

            total_amount=total
        )

        for product_id, quantity in cart.items():

            product = Product.objects.get(
                id=product_id
            )

            OrderItem.objects.create(

                order=order,

                product=product,

                quantity=quantity,

                price=product.discounted_price

            )

        request.session['cart'] = {}

        return redirect(
            'order_success'
        )

    return render(
        request,
        "checkout.html",
        {
            "products": products,
            "total": total
        }
    )



def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')


def wishlist(request):

    if not request.user.is_authenticated:
        return redirect('login')

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


def remove_wishlist(request, wishlist_id):

    wishlist_item = Wishlist.objects.get(
        id=wishlist_id
    )

    wishlist_item.delete()

    return redirect('wishlist')



@login_required
def add_review(request, product_id):

    if request.method == 'POST':

        product = Product.objects.get(id=product_id)

        rating = request.POST.get('rating')

        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment
        )

    return redirect(
        'product_detail',
        product_id=product_id
    )




from django.contrib.auth.decorators import login_required

@login_required
def profile(request):

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    order_count = Order.objects.filter(
        user=request.user
    ).count()

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'profile.html',
        {
            'wishlist_count': wishlist_count,
            'order_count': order_count,
            'orders': orders
        }
    )




def order_success(request):

    return render(
        request,
        'order_success.html'
    )

def increase_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def remove_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')
