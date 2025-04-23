import { CommonModule, NgIf, NgForOf } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { CartService } from '../../services/cart.service';
import { Product } from '../../models';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, NgIf, NgForOf],
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss']
})
export class CartComponent implements OnInit {
  cartItems: (Product & { quantity: number })[] = [];

  constructor(private cartService: CartService) {}

  ngOnInit(): void {
    this.cartService.getCart().subscribe((items: any[]) => {
      this.cartItems = items.map(item => ({
        ...item.product,
        quantity: item.quantity
      }));
    });
  }

  increase(item: any): void {
    item.quantity++;
    this.cartService.updateCart(item.id, item.quantity).subscribe();
  }

  decrease(item: any): void {
    if (item.quantity > 1) {
      item.quantity--;
      this.cartService.updateCart(item.id, item.quantity).subscribe();
    }
  }

  getTotal(): number {
    return this.cartItems.reduce((sum, item) => {
      return sum + (item.price * item.quantity);
    }, 0);
  }
}