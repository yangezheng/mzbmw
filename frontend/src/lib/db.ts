import { supabase } from "@/lib/supabaseClient"

type HistoryItem = {
  input: number
  result: number
  created_at: string
}

export async function getUserHistory(userId: string): Promise<HistoryItem[]> {
  const { data, error } = await supabase
    .from("calcu_usage")
    .select("input, result, created_at")
    .eq("user_id", userId)
    .order("created_at", { ascending: false })

  if (error) {
    console.error("Error fetching history:", error)
    return []
  }

  return data as HistoryItem[]
}

export async function insertUsage(userId: string, input: number, result: number) {
  const { error } = await supabase
    .from("calcu_usage")
    .insert([{ user_id: userId, input, result }])

  if (error) {
    console.error("Insert failed:", error)
    throw error
  }
}
