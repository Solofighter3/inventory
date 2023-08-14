from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login,logout,authenticate
from .forms import ContactForm,Itemfield,Orderform
from django.contrib import messages
from .models import YourItem,Orders,Room,Message
from django.contrib.auth.decorators import login_required
from django_pandas.io import read_frame
import plotly.express as px
import plotly
import json

# Create your views here.
def index(request):
    context={
        "inventories": YourItem.objects.all()
    }

    return render(request,"index.html",context=context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def contact(request):
    if request.method=="POST":
        contacts=ContactForm(request.POST)
        if contacts.is_valid():
            newcontact=contacts.save(commit=False)
            newcontact.save()
            messages.success(request, "Profile details updated.")
    else:
        contacts=ContactForm()
    return render(request,"contact.html",{'form':contacts})

@login_required
def products(request):
    user=request.user
    context={
        "inventories": YourItem.objects.filter(user=user),
    }

    return render(request,"userproducts.html",context=context)

@login_required
def per_product(request,pk):
    inventory=get_object_or_404(YourItem,pk=pk)
    context={
        'inventory': inventory
    }
    return render(request,"per_product.html",context=context)

@login_required
def addtoinvent(request):
    if request.method=='POST':
       addinvent=Itemfield(request.POST)
       print("hello")
       if addinvent.is_valid():
           newinvent=addinvent.save(commit=False)
           newinvent.user=request.user
           newinvent.sales_of_item=float(addinvent.data['cost_per_item']) * float(addinvent.data["ammount_sold"])
           newinvent.save()
           messages.success(request, "Product is added")
           return redirect("myproducts")
    else:
        addinvent=Itemfield()
    return render(request,"addproduct.html",{'form':addinvent})

@login_required
def delete_item(request,pk):
    item=get_object_or_404(YourItem,pk=pk)
    if request.user==item.user:
       item.delete()
       messages.success(request, "Product is deleted")
    else:
        messages.success(request, "You cannot delete this product")
        return redirect('index')
    return redirect('myproducts')

@login_required
def update_itemsa(request,pk):
    invent=get_object_or_404(YourItem,pk=pk)
    if request.method =="POST":
            update_item=Itemfield(request.POST)
            if update_item.is_valid():
                if request.user==invent.user:
                   invent.name=update_item.data["name"]
                   invent.cost_per_item=update_item.data["cost_per_item"]
                   invent.ammount_in_stock=update_item.data["ammount_in_stock"]
                   invent.ammount_sold=update_item.data["ammount_sold"]
                   invent.sales_of_item=float(invent.cost_per_item) * float(invent.ammount_sold)
                   invent.save()
                   messages.success(request, "Product is updated")
                   return redirect("index")
                else:
                    messages.success(request, "You cannot update")
                    return redirect('index')
    else:
        update_item=Itemfield(instance=invent)
    return render(request,"updateitem.html",{"form":update_item})


@login_required
def orders(request,pk):
    invent=get_object_or_404(YourItem,pk=pk)

    if request.method=='POST':
       Orderinvent=Orderform(request.POST)

       print("hello")
       if Orderinvent.is_valid():
           Orderinventnew=Orderinvent.save(commit=False)
           Orderinventnew.Orderer_Username=request.user
           Orderinventnew.product_ordered=invent
           Orderinventnew.save()
           messages.success(request, "Product is ordered")
           return redirect("index")
    else:
        Orderinvent=Orderform(initial={'Orderer_Username':request.user,'product_ordered':invent})
    return render(request,"order.html",{'form':Orderinvent})

@login_required
def ordermessage(request,pk):
    invent=get_object_or_404(YourItem,pk=pk)
    if Orders.objects.filter(product_ordered=invent,Orderer_Username=request.user).exists():
        order=Orders.objects.filter(product_ordered=invent,Orderer_Username=request.user)
        for i in order:
           print(i.ordername)
           context={
           'orders':order
            }
    else:
        messages.success(request, "Order the product to get response")
        return redirect("index")
    return render(request,"ordermsg.html",context=context)

@login_required
def ordermessagead(request,pk):
    invent=get_object_or_404(YourItem,pk=pk)
    if Orders.objects.filter(product_ordered=invent).exists():
        order=Orders.objects.filter(product_ordered=invent)
        for i in order:
           print(i.ordername)
           context={
           'orders':order
            }
    else:
        messages.success(request, "Order the product to get response")
        return redirect("index")
    return render(request,"ordermsg.html",context=context)
@login_required
def details(request):
    items=YourItem.objects.filter(user=request.user)
    df=read_frame(items)
    salesgraph=df.groupby(by="last_sales_date",as_index=False,sort=False)['sales_of_item'].sum()
    salesgraph=px.line(salesgraph,x=salesgraph.last_sales_date,y=salesgraph.sales_of_item,title="sales trend")
    salesgraph=json.dumps(salesgraph,cls=plotly.utils.PlotlyJSONEncoder)

    best_performing=df.groupby(by='name').sum().sort_values(by="ammount_sold")
    best_performing=px.bar(best_performing,x=best_performing.index,y=best_performing.ammount_sold,title="best sold")
    best_performing=json.dumps(best_performing,cls=plotly.utils.PlotlyJSONEncoder)

    most_items=df.groupby(by='name').sum().sort_values(by='ammount_in_stock')
    most_items=px.pie(most_items,names=most_items.index,values=most_items.ammount_in_stock,title="most product")
    most_items=json.dumps(most_items,cls=plotly.utils.PlotlyJSONEncoder)
    context={
        'salesgraph':salesgraph,
        'bestperforming':best_performing,
        'most_items':most_items
    }
    
    return render(request,"dashboard.html",context=context)

@login_required
def messageser(request,id):
    order=Orders.objects.get(pk=id)
    print(order)
    val=[c.slug for c in Room.objects.all()]
    if id not in val:
         room=Room.objects.create(name=order,slug=id)
    else:
        room=Room.objects.get(name=order,slug=id)
        messages=Message.objects.filter(room=room)[0:25]

   
    return render(request,"chat.html",{"room_name":id,"messages":messages})