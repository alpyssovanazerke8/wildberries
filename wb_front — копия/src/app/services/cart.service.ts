import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environments';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private apiUrl = `${environment.apiUrl}/cart/`;

  constructor(private http: HttpClient) {}

  getCart(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  addToCart(productId: number, quantity = 1): Observable<any> {
    return this.http.post(`${this.apiUrl}`, {
      product_id: productId,
      quantity
    });
  }

  updateCart(productId: number, quantity: number): Observable<any> {
    return this.http.put(`${this.apiUrl}${productId}/`, { quantity });
  }

  removeFromCart(productId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${productId}/`);
  }

  isInCart(productId: number): boolean {
    // Заглушка, если не реализовано
    return false;
  }
}