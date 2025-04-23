import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Product } from '../../models';
import { ProductService } from '../../services/product.service';
import { FavoritesService } from '../../services/favorites.service';
import { CartService } from '../../services/cart.service';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-detail.component.html',
  styleUrl: './product-detail.component.css'
})
export class ProductDetailComponent implements OnInit {
  product!: Product;
  isInCart: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private productService: ProductService,
    private cartService: CartService,
    private favoritesService: FavoritesService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.productService.getProductById(id).subscribe(data => {
      this.product = data;
      this.isInCart = this.cartService.isInCart(data.id);
    });
  }

  goToCart(): void {
    this.router.navigate(['/cart']);
  }

  toggleCart(): void {
    if (this.product) {
      this.cartService.addToCart(this.product.id).subscribe({
        next: () => {
          this.isInCart = true;
        },
        error: (err) => {
          console.error('Ошибка при добавлении в корзину:', err);
        }
      });
    }
  }

  toggleFavorite(): void {
    if (!this.product) return;

    this.favoritesService.toggleFavorite(this.product.id).subscribe({
      next: () => {
        this.product.isFavorite = !this.product.isFavorite;
      },
      error: err => {
        console.error('Ошибка при добавлении в избранное:', err);
      }
    });
  }
}