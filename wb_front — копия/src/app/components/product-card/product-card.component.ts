import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CartService } from '../../services/cart.service';
import { Product } from '../../models';
import { FavoritesService } from '../../services/favorites.service';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './product-card.component.html',
  styleUrl: './product-card.component.css'
})
export class ProductCardComponent implements OnInit {
  @Input() product!: Product;
  isInCart = false;
  isFavorite = false;

  constructor(
    private cartService: CartService,
    private favoritesService: FavoritesService
  ) {}

  ngOnInit(): void {
    this.isInCart = this.cartService.isInCart(this.product.id);
    this.isFavorite = !!this.product.isFavorite;
  }

  toggleCart(): void {
    if (!this.product) return;
  
    if (this.isInCart) {
      // Удалить товар с backend
      this.cartService.removeFromCart(this.product.id).subscribe({
        next: () => {
          this.isInCart = false;
        },
        error: (err) => {
          console.error('Ошибка удаления из корзины:', err);
        }
      });
    } else {
      // Добавить товар на backend
      this.cartService.addToCart(this.product.id).subscribe({
        next: () => {
          this.isInCart = true;
        },
        error: (err) => {
          console.error('Ошибка добавления в корзину:', err);
        }
      });
    }
  }

  toggleFavorite(): void {
    this.favoritesService.toggleFavorite(this.product.id).subscribe(() => {
      this.product.isFavorite = !this.product.isFavorite;
    });
  }
}