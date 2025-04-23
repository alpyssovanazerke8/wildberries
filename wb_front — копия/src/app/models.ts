export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
}
export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image: string;
  rating: number;
  reviewsCount: number;
  isDiscounted?: boolean;
  oldPrice?: number;
  deliveryDate?: string;
  isFavorite?: boolean;
}
export interface Post {
  userId: number;
  id: number;
  title: string;
  body: string;
}