import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({providedIn: 'root'})
export class ApiService {
  backendUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) {}

  getProducts() { return this.http.get(this.backendUrl + 'products/'); }
  getProduct(slug: string) { return this.http.get(this.backendUrl + `products/${slug}/`); }
  login(data: any) { return this.http.post(this.backendUrl + 'token/', data); }
  addToCart(productId: number, quantity: number) { return this.http.post(this.backendUrl + 'cart/add/', { product_id: productId, quantity }); }
  getCart() { return this.http.get(this.backendUrl + 'cart/'); }
  placeOrder(orderData: any) { return this.http.post(this.backendUrl + 'orders/', orderData); }
  getProfile() { return this.http.get(this.backendUrl + 'profile/'); }
}