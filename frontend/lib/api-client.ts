/**
 * API Client for Gemini File Search Backend
 * 
 * This module provides type-safe API calls to the FastAPI backend.
 */

import {
  UploadResponse,
  QueryResponse,
  StoreInfo,
  QueryRequest,
  UploadResponseSchema,
  QueryResponseSchema,
  StoreInfoSchema,
  ErrorResponseSchema,
} from "./api-types";
import { z } from "zod";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string
  ) {
    super(message);
    this.name = "APIError";
  }
}

/**
 * Upload a file to the File Search Store
 */
export async function uploadFile(
  file: File,
  createNewStore: boolean = false,
  storeName?: string
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("create_new_store", createNewStore.toString());
  if (storeName) {
    formData.append("store_name", storeName);
  }

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const parsed = ErrorResponseSchema.safeParse(errorData);
    throw new APIError(
      parsed.success ? parsed.data.error : "Upload failed",
      response.status,
      parsed.success ? parsed.data.detail : undefined
    );
  }

  const data = await response.json();
  return UploadResponseSchema.parse(data);
}

/**
 * Query files in a File Search Store
 */
export async function queryFiles(request: QueryRequest): Promise<QueryResponse> {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const parsed = ErrorResponseSchema.safeParse(errorData);
    throw new APIError(
      parsed.success ? parsed.data.error : "Query failed",
      response.status,
      parsed.success ? parsed.data.detail : undefined
    );
  }

  const data = await response.json();
  return QueryResponseSchema.parse(data);
}

/**
 * List all File Search Stores
 */
export async function listStores(): Promise<StoreInfo[]> {
  const response = await fetch(`${API_BASE_URL}/stores/list`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const parsed = ErrorResponseSchema.safeParse(errorData);
    throw new APIError(
      parsed.success ? parsed.data.error : "Failed to list stores",
      response.status,
      parsed.success ? parsed.data.detail : undefined
    );
  }

  const data = await response.json();
  return z.array(StoreInfoSchema).parse(data);
}

/**
 * Delete a File Search Store
 */
export async function deleteStore(storeId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/stores/${storeId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const parsed = ErrorResponseSchema.safeParse(errorData);
    throw new APIError(
      parsed.success ? parsed.data.error : "Failed to delete store",
      response.status,
      parsed.success ? parsed.data.detail : undefined
    );
  }
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<{ status: string; gemini: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new APIError("Health check failed", response.status);
  }

  return response.json();
}

export { APIError };
