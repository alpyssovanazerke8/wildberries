import { Component, OnInit } from '@angular/core';
import { Category } from '../../models';
import { CategoryService } from '../../services/category.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar-menu',
  standalone:true,
  imports: [CommonModule], 
  templateUrl: './sidebar-menu.component.html',
  styleUrls: ['./sidebar-menu.component.css']
})
export class SidebarMenuComponent implements OnInit {
  categories: Category[] = [];

  constructor(private categoryService: CategoryService) {}

  ngOnInit(): void {
    this.categoryService.getCategories().subscribe({
      next: (data: Category[]) => {
        this.categories = data;
        console.log('Категории:', data);
      },
      error: (error) => {
        console.error('Ошибка при загрузке категорий:', error);
      }
    });
  }
}