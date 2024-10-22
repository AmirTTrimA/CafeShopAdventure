class OrderFilterView(View):
    template_name = 'staff\order_list.html'

    def get(self, request):
        form = OrderFilterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            filter_type = form.cleaned_data['filter_type']
            filter_value= form.cleaned_data['filter_value']
            if filter_type!='last_order' and filter_value =='':
                form.add_error('filter_value', 'Please enter a valid value.')

            elif filter_type == 'last_order' :
                orders = Order.objects.order_by('-order_date')[:1]  # Last order
                return render(request, self.template_name, {'form': form, 'orders': orders})

            elif filter_type !='last_order' and filter_value!='':
            
            # Apply filtering based on filter type
                if filter_type == 'date':
                    import datetime
                    try:
                        date_filter = datetime.datetime.strptime(filter_value, '%Y-%m-%d')
                        orders = Order.objects.filter(order_date__date=date_filter)
                    except ValueError:
                        orders = Order.objects.none()  # Return no results on invalid date
                elif filter_type == 'status':
                    orders = Order.objects.filter(status=filter_value)
                elif filter_type == 'table_number':
                    customers = Customer.objects.filter(table_number=filter_value)
                    orders = Order.objects.filter(customer__in=customers)

                return render(request, self.template_name, {'form': form, 'orders': orders})
        
            return render(request, self.template_name, {'form': form})
