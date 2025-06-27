from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Property
from loan_calculator.forms import LoanCalculatorForm
from payment.utils import calculate_payment
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def property_list(request):
    """
    列出 Property 列表，并支持：
      - 按 location 精确匹配（下拉框里选的）
      - 按 title/description/location 模糊匹配，或 price 精确匹配（如果 search 是纯数字）
      - 按 price 升序/降序 排序
      - 分页，每页 6 条
    """

    # 1. 从 GET 参数获取筛选和排序条件
    location     = request.GET.get('location', '').strip()      # 例如: "SELANGOR"
    search       = request.GET.get('search', '').strip()        # 例如: "Elmina" 或 "420000"
    price_order  = request.GET.get('price_order', '').strip()   # "asc" 或 "desc"
    page_number  = request.GET.get('page')                      # 当前页码

    # 2. 初始 QuerySet：所有 Property
    qs = Property.objects.filter(type='sale', is_booked=False)

    # 3. 如果下拉里选了 location，就做精确匹配（choices 已限制，直接 __exact 或 __iexact 均可）
    if location:
        qs = qs.filter(location__iexact=location)

    # 4. 如果 search 不为空，就做“标题 / 描述 / 位置 模糊匹配”或“价格精确匹配”
    if search:
        # 4.1 如果 search 纯数字，就尝试把它当作 price 去精确匹配
        price_q = Q()
        if search.isdigit():
            try:
                price_value = float(search)
                price_q = Q(price__exact=price_value)
            except ValueError:
                price_q = Q()

        # 4.2 同时匹配 title / description / location 的 icontains，或 price_q
        qs = qs.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search) |
            price_q
        )

    # 5. 根据 price_order 排序
    if price_order == 'asc':
        qs = qs.order_by('price')
    elif price_order == 'desc':
        qs = qs.order_by('-price')
    else:
        # 如果没有传 price_order，就默认按最新创建（id 倒序）
        qs = qs.order_by('-id')

    # 6. 动态取前三条最新房源作为推荐
    recommended = Property.objects.filter(type='sale', is_booked=False).order_by('-id')[:3]

    # 6. 用 Paginator 分页，每页 6 条
    paginator = Paginator(qs, 6)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)



    # 7. 把 page_obj 及当前筛选/排序参数传给模板
    context = {
        'page_obj': page_obj,  # ① 把 page_obj 直接放到 context 里

        'properties': page_obj,
        'selected_location': location,
        'selected_search': search,
        'selected_price_order': price_order,
        'location_choices': Property.LOCATION_CHOICES,  # 把 choices 也传过去，若模板想动态渲染下拉
        'recommended': recommended,
    }
    return render(request, 'property_list.html', context)


def property_detail(request, pk):
    print(f"*** property_detail 被调用，pk = {pk} ***")
    property_obj = get_object_or_404(Property, pk=pk)
    print(f"*** 成功拿到 Property：{property_obj.title} ***")

    #desmond part
    form = LoanCalculatorForm(initial={'property': property_obj})
    result = None

    if request.method == 'POST':
        form = LoanCalculatorForm(request.POST)
        if form.is_valid():
            result = form.calculate()  # Assuming your form has a `.calculate()` method that returns the result
    return render(request, 'property_detail.html',
                  {'property': property_obj,
                   'form': form,
                   'result': result,
                   'payment_info': calculate_payment(property_obj),


                   })


def new_launches_view(request):
    # Get top 10 newest properties ordered by created_at (newest first)
    new_properties = Property.objects.all().order_by('-created_at')[:10]

    # Add recommended properties (you can customize this logic)
    recommended = Property.objects.all().order_by('?')[:4]  # Random 4 properties
    # OR use a different logic like:
    # recommended = Property.objects.filter(is_featured=True)[:4]  # if you have a featured field
    # recommended = Property.objects.all().order_by('-price')[:4]  # Most expensive

    context = {
        'properties': new_properties,
        'recommended': recommended,  # Add this line
        'page_title': 'New Launches',
        'is_new_launches': True,
    }
    return render(request, 'new_launches.html', context)

def advertise_view(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        ad_type = request.POST.get('ad_type')
        budget = request.POST.get('budget')
        message = request.POST.get('message')

        # Send email (optional - configure your email settings first)
        try:
            email_message = f"""
            New Advertising Request:

            Name: {name}
            Email: {email}
            Phone: {phone}
            Company: {company}
            Ad Type: {ad_type}
            Budget: {budget}
            Message: {message}
            """

            send_mail(
                'New Advertising Request - MyPropertizz',
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['your-admin@email.com'],  # Replace with your admin email
                fail_silently=True,
            )
            messages.success(request,
                             'Thank you! Your advertising request has been submitted. We will contact you soon.')
        except:
            messages.success(request, 'Thank you! Your request has been submitted.')

        return redirect('proplistpage:advertise')

    return render(request, 'advertise.html')


def guides_insights_view(request):
    return render(request, 'guides_insights.html')
