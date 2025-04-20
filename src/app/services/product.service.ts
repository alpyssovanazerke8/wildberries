import { Injectable } from '@angular/core';
import { Product } from '../models';


@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private products: Product[] = [
    {
      id: 1,
      name: 'Салфетки из микрофибры 30x30',
      description: '30 штук, микрофибра, многоцветные',
      price: 368,
      oldPrice: 487,
      image: 'https://via.placeholder.com/300x300?text=Салфетки',
      rating: 4.8,
      reviewsCount: 141564,
      isDiscounted: true,
      deliveryDate: 'Завтра'
    },
    // добавь другие товары
  ];

  getProducts(): Product[] {
    return this.products;
  }

  getProductById(id: number): Product | undefined {
    return this.products.find(p => p.id === id);
  }
}
