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
            item.description =request.Post.get('Product description')
            item.price = request.Post.get('Product Price')
            item.category = request.Post.get('Product cat')
            item.save()
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'Changes saved successfully'})
         else:
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'product dose not exist'})
