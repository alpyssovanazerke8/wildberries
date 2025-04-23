import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environments';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
    private tokenKey = 'access_token';
    private refreshKey = 'refresh_token';
    private apiUrl = `${environment.apiUrl}auth/token/`;
    
    constructor(private http: HttpClient, private router: Router) {}

    login(username: string, password: string) {
        return this.http.post<any>(this.apiUrl, {
          username,
          password
        });
      }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.refreshKey);
    this.router.navigate(['/login']);
  }

  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}