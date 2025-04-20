import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-banner',
  imports: [CommonModule],
  templateUrl: './banner.component.html',
  styleUrl: './banner.component.css'
})
export class BannerComponent {
  banners: string[] = [
    'https://via.placeholder.com/300x150?text=Banner+1',
    'https://via.placeholder.com/300x150?text=Banner+2',
    'https://via.placeholder.com/300x150?text=Banner+3',
    'https://via.placeholder.com/300x150?text=Banner+4',
  ];

}
