import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private cart: any[] = [];
  getCart() {
    return this.cart;
  }
  addToCart(product: any) {
    if (!this.cart.find(p => p.id === product.id)) {
      this.cart.push(product);
    }
  }

  removeFromCart(productId: number) {
    this.cart = this.cart.filter(p => p.id !== productId);
  }

  isInCart(productId: number): boolean {
    return this.cart.some(p => p.id === productId);
  }


  constructor() { }
}
