import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { api } from "@/lib/api"

// Common electronic component MPNs as examples
const EXAMPLE_MPNS = [
  { name: "IFR530", description: "VISHAY MOSFET" },
  { name: "BD42754FPJ-CE2", description: "ROHM LDO" },
  { name: "TLV733P-Q1", description: "TI LDO" }
]

export function DatasheetDownloader() {
  const [mpn, setMpn] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const downloadDatasheet = async () => {
    if (!mpn.trim()) {
      setError("Please enter a valid MPN")
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Using axios for blob response
      const response = await api.post("/api/download-datasheet", 
        { MPN: mpn }, 
        { responseType: 'blob' }
      )
      
      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]))
      
      // Create a temporary link to trigger download
      const link = document.createElement('a')
      link.href = url
      
      // Get filename from content-disposition header or use MPN as filename
      const contentDisposition = response.headers['content-disposition']
      const filename = contentDisposition
        ? contentDisposition.split('filename=')[1].replace(/"/g, '')
        : `${mpn}.pdf`
        
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      
      // Clean up
      link.parentNode?.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      console.error('Download error:', err)
      setError(err.response?.data?.detail || 'Failed to download datasheet')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Download Component Datasheet</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Input
            value={mpn}
            onChange={(e) => setMpn(e.target.value)}
            placeholder="Enter Manufacturer Part Number (MPN)"
          />
        </div>
        
        <div className="text-sm text-gray-500 mb-2">
          Examples: Click to try
          <div className="flex flex-wrap gap-2 mt-2">
            {EXAMPLE_MPNS.map((example) => (
              <button
                key={example.name}
                onClick={() => setMpn(example.name)}
                className="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-md transition-colors flex flex-col items-center"
              >
                <span className="font-medium">{example.name}</span>
                <span className="text-xs text-gray-500">{example.description}</span>
              </button>
            ))}
          </div>
        </div>
        
        {error && <p className="text-sm text-red-500">{error}</p>}
        
        <Button 
          onClick={downloadDatasheet} 
          disabled={loading || !mpn.trim()}
          className="w-full"
        >
          {loading ? "Downloading..." : "Download Datasheet"}
        </Button>
      </CardContent>
    </Card>
  )
} 