import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../models';
import { environment } from '../../environments/environments';

@Injectable({ providedIn: 'root' })
export class FavoritesService {
  private apiUrl = `${environment.apiUrl}/favorites/`;

  constructor(private http: HttpClient) {}

  getFavorites(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl);
  }
  toggleFavorite(productId: number): Observable<any> {
    return this.http.post(this.apiUrl, { product_id: productId });
  }
}