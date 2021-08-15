from django.shortcuts import render

from API.models import Product, ProductsPrices
from django.core.paginator import Paginator

contador = 0

def index(request):
    allProducts = Product.objects.get_queryset().order_by('id') #pegando os produtos e ordenando pelo id
    produtos = Paginator(allProducts,10) #paginando os produtos de 10 em 10

    # variaveis de inicializacao para controlar a paginacao:
    back_page_number=1
    next_page_number=1

    page = produtos.page(1)

    # --- para tratar a parte de versionamento de periodos
    product_id_for_periods = request.GET.get("product_id_for_periods")
    productPeriodMap = None
    if(product_id_for_periods):
        print("ID -> ",product_id_for_periods)
        productsPrices = list(ProductsPrices.objects.filter(product=product_id_for_periods))
        if(productsPrices):

            productPeriodMap = {
                "id": int(product_id_for_periods),
                "items": productsPrices,
                "helloTest":"hello",
            }
            # print("\nproductPeriodMap-> ", productPeriodMap.id)
            # print("products prices: ",productsPrices,"dir: ",dir(productsPrices.values))

    # --- para tratar a parte de busca de produtos
    query = request.GET.get('search') #aqui vai receber o que vier da entrada de busca de produtos
    if(query): #se a query existir quer dizer que foi pesquisado algo
        allProducts = Product.objects.filter(description__icontains=query) #pega todos os produtos com essa palavra

        # senao houver ninguem em produtos ele verifica no nome da loja:
        if(len(allProducts)==0):
            allProducts = Product.objects.filter(storeName__icontains=query)
            produtos = Paginator(allProducts, 10)
            page = produtos.page(1)
        else: #se houver, ele pega esses produtos
            produtos = Paginator(allProducts, 10)
            page = produtos.page(1)
    # --- Fim busca produtos

    # aqui vai receber um "sinal" do botao de voltar da paginacao e atualizar a pagina
    goNext = request.POST.get('next-btn')
    if(goNext):
        back_page_number=goNext #setando o numero da pagina anterior como o atual ate entao
        next_page_number = int(goNext)+1 #incrementando o valor para o da pagina atual
        page = produtos.page(next_page_number) #indo para a pagina em si

    # mesma coisa que o anterior:
    goBack = request.POST.get('back-btn')
    if (goBack):
        if(int(goBack)-1>0):
            next_page_number=goBack
            page = produtos.get_page(int(goBack))
            back_page_number = int(goBack) - 1

    # passando as variaveis para o contexto do template:
    context = {
        'produtos': page.object_list,
        'back_page_number': back_page_number,
        'next_page_number': next_page_number,
        'productPeriodMap': productPeriodMap,
    }
    return render(request, 'indexCommercial.html', context)

def getProductsInfo(searchTerm, carajasCheck = True, leroyCheck = True, tupanCheck = True):
    allProducts = {}
    if carajasCheck:
        allProducts['carajas'] = Product.objects.filter(description__icontains=searchTerm, storeName__icontains="Carajás")
    
    if leroyCheck:
        allProducts['leroy'] = Product.objects.filter(description__icontains=searchTerm, storeName__icontains="Leroy Merlin")
    
    if tupanCheck:
        allProducts['tupan'] = Product.objects.filter(description__icontains=searchTerm, storeName__icontains="Tupan")
    
    return allProducts

def root(request):
    return render(request, 'root.html')