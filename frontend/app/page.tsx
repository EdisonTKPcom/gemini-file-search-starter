"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { Upload, Send, File, Loader2, CheckCircle, AlertCircle } from "lucide-react";
import { uploadFile, queryFiles } from "@/lib/api-client";
import { FileInfo, QueryResponse } from "@/lib/api-types";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface UploadedFile extends FileInfo {
  localName: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: QueryResponse["citations"];
}

export default function Home() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [currentStore, setCurrentStore] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [query, setQuery] = useState("");
  const [isQuerying, setIsQuerying] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    setIsUploading(true);
    const file = files[0];

    try {
      // Upload to existing store or create new one
      const response = await uploadFile(
        file,
        currentStore === null, // Create new store if none exists
        currentStore || undefined
      );

      if (response.success && response.file_info && response.store_name) {
        // Update store name if new
        if (!currentStore) {
          setCurrentStore(response.store_name);
        }

        // Add to uploaded files list
        setUploadedFiles((prev) => [
          ...prev,
          {
            ...response.file_info,
            localName: file.name,
          },
        ]);

        toast({
          title: "File uploaded",
          description: `${file.name} has been uploaded successfully.`,
        });
      }
    } catch (error) {
      console.error("Upload error:", error);
      toast({
        title: "Upload failed",
        description: error instanceof Error ? error.message : "Failed to upload file",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim() || !currentStore) {
      toast({
        title: "Cannot submit query",
        description: currentStore ? "Please enter a question" : "Please upload a file first",
        variant: "destructive",
      });
      return;
    }

    setIsQuerying(true);
    
    // Add user message
    const userMessage: Message = {
      role: "user",
      content: query,
    };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");

    try {
      const response = await queryFiles({
        query: query,
        store_name: currentStore,
        temperature: 0.1,
      });

      // Add assistant message
      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
        citations: response.citations,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Query error:", error);
      toast({
        title: "Query failed",
        description: error instanceof Error ? error.message : "Failed to query files",
        variant: "destructive",
      });
      
      // Remove the user message if query failed
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setIsQuerying(false);
    }
  };

  const detectCodeLanguage = (source: string, text: string): string => {
    const ext = source.split('.').pop()?.toLowerCase();
    const langMap: Record<string, string> = {
      'py': 'python',
      'js': 'javascript',
      'ts': 'typescript',
      'jsx': 'jsx',
      'tsx': 'tsx',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'go': 'go',
      'rs': 'rust',
      'rb': 'ruby',
      'php': 'php',
      'swift': 'swift',
      'kt': 'kotlin',
      'cs': 'csharp',
    };
    
    return langMap[ext || ''] || 'text';
  };

  const isCodeFile = (filename: string): boolean => {
    const codeExtensions = ['py', 'js', 'ts', 'jsx', 'tsx', 'java', 'cpp', 'c', 'go', 'rs', 'rb', 'php', 'swift', 'kt', 'cs'];
    const ext = filename.split('.').pop()?.toLowerCase();
    return ext ? codeExtensions.includes(ext) : false;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/20">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
                Gemini File Search
              </h1>
              <p className="text-sm text-muted-foreground">
                Upload files and ask questions with AI-powered search
              </p>
            </div>
            
            {/* Upload button */}
            <div>
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileUpload}
                accept=".pdf,.docx,.txt,.json,.py,.js,.ts,.java,.cpp,.c,.go,.rs,.md"
                className="hidden"
              />
              <Button
                onClick={() => fileInputRef.current?.click()}
                disabled={isUploading}
                className="gap-2"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload className="h-4 w-4" />
                    Upload File
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Sidebar - File List */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Uploaded Files</CardTitle>
                <CardDescription>
                  {uploadedFiles.length === 0 
                    ? "No files uploaded yet" 
                    : `${uploadedFiles.length} file(s) indexed`}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {uploadedFiles.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <File className="h-12 w-12 mx-auto mb-3 opacity-50" />
                    <p className="text-sm">Upload a file to get started</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {uploadedFiles.map((file, index) => (
                      <div
                        key={index}
                        className="flex items-start gap-3 p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
                      >
                        <div className="flex-shrink-0 mt-1">
                          {file.status === "ready" ? (
                            <CheckCircle className="h-4 w-4 text-green-500" />
                          ) : (
                            <Loader2 className="h-4 w-4 animate-spin text-primary" />
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">
                            {file.localName}
                          </p>
                          <p className="text-xs text-muted-foreground capitalize">
                            {file.status}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Main Content - Chat Interface */}
          <div className="lg:col-span-2">
            <Card className="h-[calc(100vh-12rem)] flex flex-col">
              <CardHeader>
                <CardTitle>Ask Questions</CardTitle>
                <CardDescription>
                  Ask anything about your uploaded files
                </CardDescription>
              </CardHeader>
              
              {/* Messages */}
              <CardContent className="flex-1 overflow-y-auto space-y-4">
                {messages.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-muted-foreground">
                    <div className="text-center">
                      <Send className="h-12 w-12 mx-auto mb-3 opacity-50" />
                      <p>Start a conversation by asking a question</p>
                    </div>
                  </div>
                ) : (
                  messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${
                        message.role === "user" ? "justify-end" : "justify-start"
                      }`}
                    >
                      <div
                        className={`max-w-[85%] rounded-lg p-4 ${
                          message.role === "user"
                            ? "bg-primary text-primary-foreground"
                            : "bg-muted"
                        }`}
                      >
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                        
                        {/* Citations */}
                        {message.citations && message.citations.length > 0 && (
                          <div className="mt-4 pt-4 border-t border-border/50">
                            <p className="text-xs font-semibold mb-2 opacity-70">
                              Sources:
                            </p>
                            <div className="space-y-2">
                              {message.citations.map((citation, citIndex) => (
                                <div
                                  key={citIndex}
                                  className="text-xs bg-background/50 rounded p-2"
                                >
                                  <p className="font-medium mb-1 flex items-center gap-1">
                                    <File className="h-3 w-3" />
                                    {citation.source}
                                  </p>
                                  {isCodeFile(citation.source) ? (
                                    <SyntaxHighlighter
                                      language={detectCodeLanguage(citation.source, citation.text)}
                                      style={vscDarkPlus}
                                      customStyle={{
                                        margin: 0,
                                        padding: "0.5rem",
                                        fontSize: "0.75rem",
                                        borderRadius: "0.25rem",
                                      }}
                                    >
                                      {citation.text}
                                    </SyntaxHighlighter>
                                  ) : (
                                    <p className="opacity-80 italic">
                                      &ldquo;{citation.text}&rdquo;
                                    </p>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))
                )}
                
                {isQuerying && (
                  <div className="flex justify-start">
                    <div className="bg-muted rounded-lg p-4">
                      <Loader2 className="h-5 w-5 animate-spin" />
                    </div>
                  </div>
                )}
              </CardContent>

              {/* Query Input */}
              <CardContent className="border-t pt-4">
                <form onSubmit={handleQuery} className="flex gap-2">
                  <Input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={
                      currentStore
                        ? "Ask a question about your files..."
                        : "Upload a file first..."
                    }
                    disabled={!currentStore || isQuerying}
                    className="flex-1"
                  />
                  <Button
                    type="submit"
                    disabled={!currentStore || !query.trim() || isQuerying}
                    size="icon"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
