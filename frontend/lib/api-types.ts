import { z } from "zod";

// API response schemas
export const CitationSchema = z.object({
  text: z.string(),
  source: z.string(),
  uri: z.string().optional(),
});

export const FileInfoSchema = z.object({
  name: z.string(),
  file_id: z.string().optional(),
  status: z.string(),
  uploaded_at: z.string(),
});

export const UploadResponseSchema = z.object({
  success: z.boolean(),
  message: z.string(),
  file_info: FileInfoSchema.optional(),
  store_name: z.string().optional(),
});

export const QueryResponseSchema = z.object({
  answer: z.string(),
  citations: z.array(CitationSchema),
});

export const StoreInfoSchema = z.object({
  name: z.string(),
  display_name: z.string(),
  created_at: z.string().optional(),
});

export const ErrorResponseSchema = z.object({
  error: z.string(),
  detail: z.string().optional(),
});

// Request schemas
export const QueryRequestSchema = z.object({
  query: z.string(),
  store_name: z.string(),
  temperature: z.number().min(0).max(1).optional(),
});

// TypeScript types derived from schemas
export type Citation = z.infer<typeof CitationSchema>;
export type FileInfo = z.infer<typeof FileInfoSchema>;
export type UploadResponse = z.infer<typeof UploadResponseSchema>;
export type QueryResponse = z.infer<typeof QueryResponseSchema>;
export type StoreInfo = z.infer<typeof StoreInfoSchema>;
export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;
export type QueryRequest = z.infer<typeof QueryRequestSchema>;
