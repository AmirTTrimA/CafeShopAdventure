class ProductUpdateView(View):

    def get(self, request):
         items=MenuItem.objects.all()
         cats=Category.objects.all()
         return render(request,'Edit-product.html',{'massage':'','items':items,'cats':cats})
    
    def post(self, request):
         name_i = request.get('Prodcut Name')
         item=MenuItem.objects.get(name=name_i)
         items=MenuItem.objects.all()
         cats=Category.objects.all()
         if item:
            item.description =request.POST.get('Product Price')
            item.category = request.POST.get('Product cat')
            item.save()
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'Changes saved successfully'})
         else:
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'product dose not exist'})
        
class Add_product(View):

    def get(self, request):
        cats=Category.objects.all()
        return render(request, "add-product.html",{'cats':cats})
    
    def post(self, request):
         cats=Category.objects.all()
         Product_Name=request.POST.get('Product Name')
         Product_cat=request.POST.get('Product cat')
         Product_description = request.POST.get('Product description')
         Product_Price=request.POST.get('Product Price')
         item=MenuItem(name=Product_Name,description=Product_description,price=Product_Price,category=Product_cat)
         item.save()
         return render(request, "add-product.html",{'cats':cats})
