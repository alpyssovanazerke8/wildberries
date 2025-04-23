import { Component, OnInit } from '@angular/core';
import { CartService } from '../../services/cart.service';
import { FavoritesService } from '../../services/favorites.service';
import { Product } from '../../models';

@Component({
  selector: 'app-profile',
  standalone:true,
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  balance: number = 0;
  favoritesCount: number = 0;
  toReviewCount: number = 0;

  constructor(
    private cartService: CartService,
    private favoritesService: FavoritesService
  ) {}

  ngOnInit(): void {
    // Получаем избранные товары с бэка
    this.favoritesService.getFavorites().subscribe((favorites: Product[]) => {
      this.favoritesCount = favorites.length;
    });

    // Получаем количество товаров в корзине
    this.cartService.getCart().subscribe((cartItems: any[]) => {
      this.toReviewCount = cartItems.length;
    });
  }
}