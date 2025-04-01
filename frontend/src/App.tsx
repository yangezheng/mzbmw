import { useEffect, useState } from "react"
import { supabase } from "@/lib/supabaseClient"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { api } from "@/lib/api"
import { getUserHistory, insertUsage } from "./lib/db"

type HistoryItem = {
  input: number
  result: number
  created_at: string
}

function App() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [user, setUser] = useState<any>(null)
  const [input, setInput] = useState("")
  const [result, setResult] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState<any[]>([])

  // Track session on load
  useEffect(() => {
    const getUser = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      setUser(session?.user || null)
    }
    getUser()

    // Realtime session updates
    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user || null)
    })

    return () => listener.subscription.unsubscribe()
  }, [])


  // Fetch user history from Supabase
  useEffect(() => {
    if (user) {
      getUserHistory(user.id).then(setHistory)
    }
  }, [user])

  // Sign up and sign in functions
  const signUp = async () => {
    const { error } = await supabase.auth.signUp({ email, password })
    if (error) alert(error.message)
    else alert("Check your email for the confirmation link!")
  }

  const signIn = async () => {
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) alert(error.message)
  }

  const signOut = async () => {
    await supabase.auth.signOut()
  }

  const calculate = async () => {
    setLoading(true)
    try {
      const { data } = await api.post("/api/calculate", { input })
      setResult(data.result)

      // this writes the result to the database
      if (user) {
        await insertUsage(user.id, parseFloat(input), data.result)
      }

      // Refresh history
      setHistory((prev) => [
        { input: parseFloat(input), result: data.result, created_at: new Date().toISOString() },
        ...prev,
      ])

    } catch (err) {
      alert("Failed to calculate.")
    } finally {
      setLoading(false)
    }
  }


  return (

    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md p-6 space-y-4 shadow-lg">
        {!user ? (
          <>
            <h2 className="text-xl font-bold text-center">Login or Sign Up</h2>
            <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <Button onClick={signIn}>Login</Button>
            <Button variant="secondary" onClick={signUp}>Sign Up</Button>
          </>
        ) : (
          <>
            <h2 className="text-xl font-bold text-center">Welcome, {user.email}</h2>
            <Input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Enter a number" />
            <Button onClick={calculate} disabled={loading}>
              {loading ? "Calculating..." : "Submit"}
            </Button>


            {result !== null && (
              <CardContent>
                <p>Result: <strong>{result}</strong></p>
              </CardContent>
            )}
            {history.length > 0 && (
              <div className="pt-4 border-t mt-4">
                <h3 className="text-lg font-semibold mb-2">Your History</h3>
                <div className="space-y-2">
                  {history.slice(0,5).map((item, i) => (
                    <div key={i} className="text-sm text-gray-700 bg-gray-100 p-2 rounded shadow-sm">
                      <div>
                        <strong>Input:</strong> {item.input} → <strong>Result:</strong> {item.result}
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(item.created_at).toLocaleString()}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <Button variant="destructive" onClick={signOut}>Logout</Button>


          </>
        )}
      </Card>
    </div>
  )
}

export default App
