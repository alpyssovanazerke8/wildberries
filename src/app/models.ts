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
}
