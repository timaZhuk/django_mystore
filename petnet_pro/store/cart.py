from django.conf import settings

from .models import Product

#-----Cart object------------
# Cart take on object=request
class Cart(object):

    def __init__(self, request):
        # create a session object information about browser or user
        self.session = request.session
        # create cart instance, we get session Id from settings
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # empty cart 'object' = dictionary
            cart = self.session[settings.CART_SESSION_ID] = {} 

        self.cart = cart

    #---- iteration function ---------------------------
    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
    
        for item in self.cart.values():
            item['total_price'] = int(item['product'].price*item['quantity'])/100

            yield item
    
    #---- adding together quantity of similar products
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
    # ------ save the modified cart and say to server about changes--- 
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    # -------  add function to the cart class ------------------------------
    def add(self, product_id, quantity = 1, update_quantity = False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':int(quantity), 'id':product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        
        self.save()
    
    #  -------- remove the item from cart ------------------------------ 
    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]

            self.save()
    #---------claer() function for cart-----------------------
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    #---------------------------------------------------------------
    # -----------------------------------------------------
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk = p)
        return sum(item['product'].price * item['quantity'] for item in self.cart.values())/100
    
    
    

     
    






        
