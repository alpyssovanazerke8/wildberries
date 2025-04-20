import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-sidebar-menu',
  imports: [CommonModule],
  templateUrl: './sidebar-menu.component.html',
  styleUrl: './sidebar-menu.component.css'
})
export class SidebarMenuComponent {
  categories = [
    { icon: '💸', label: 'РАСПРОДАЖА' },
    { icon: '👗', label: 'Женщинам' },
    { icon: '👟', label: 'Обувь' },
    { icon: '✂️', label: 'Детям' },
    { icon: '👔', label: 'Мужчинам' },
    { icon: '🏠', label: 'Дом' },
  ];

}
