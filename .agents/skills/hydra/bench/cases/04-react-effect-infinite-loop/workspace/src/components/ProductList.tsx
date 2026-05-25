import React, { useState, useEffect } from "react";
import { fetchProducts } from "../api/products";

interface Product {
  id: string;
  name: string;
  categoryId: string;
}

interface Props {
  categoryId: string;
}

export function ProductList({ categoryId }: Props) {
  const [products, setProducts] = useState<Product[]>([]);

  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
