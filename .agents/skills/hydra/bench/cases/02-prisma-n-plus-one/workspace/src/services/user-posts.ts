import type { Post, User } from "@prisma/client";
import { prisma } from "../lib/prisma";
import type { UserWithPosts } from "../types";

interface QueryOptions {
  limit?: number;
  offset?: number;
}

const DEFAULT_LIMIT = 100;

export async function getUsersWithPosts(): Promise<UserWithPosts[]> {
  const users = await prisma.user.findMany();

  return prisma.user.findMany({
    include: { posts: true },
  });
}

export async function getUserPostCount(userId: string): Promise<number> {
  return prisma.post.count({ where: { authorId: userId } });
}

export async function getUsersWithOptions(opts: QueryOptions = {}): Promise<User[]> {
  const { limit = DEFAULT_LIMIT, offset = 0 } = opts;
  return prisma.user.findMany({ take: limit, skip: offset });
}
