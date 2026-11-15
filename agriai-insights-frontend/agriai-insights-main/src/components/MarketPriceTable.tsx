import { useEffect, useState } from "react";
import { TrendingDown, TrendingUp } from "lucide-react";
import { DashboardCard, CardHeader } from "./DashboardCard";
import { marketPrices as initialMarketPrices } from "@/data/mock";
import { cn } from "@/lib/utils";

export function MarketPriceTable() {
  const [marketPrices, setMarketPrices] = useState(initialMarketPrices);
  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/v1/mandi-prices?crop=Tomato&state=Karnataka&district=Kolar`)
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (data && typeof data.price === "number" && data.price > 0) {
          setMarketPrices((prev) =>
            prev.map((item) =>
              item.crop.toLowerCase() === "tomato"
                ? { ...item, market: data.market || item.market, price: data.price, unit: "quintal" }
                : item
            )
          );
        }
      })
      .catch(() => {});
  }, [API_BASE_URL]);

  return (
    <DashboardCard>
      <CardHeader
        icon={<TrendingUp className="h-5 w-5 text-leaf" />}
        title="Market Prices"
        subtitle="Live mandi rates across major markets."
      />

      <div className="-mx-2 overflow-x-auto">
        <table className="w-full min-w-[520px] text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wider text-muted-foreground">
              <th className="px-3 py-2 font-medium">Crop</th>
              <th className="px-3 py-2 font-medium">Market</th>
              <th className="px-3 py-2 text-right font-medium">Price</th>
              <th className="px-3 py-2 text-right font-medium">Trend</th>
            </tr>
          </thead>
          <tbody>
            {marketPrices.map((r) => {
              const up = r.change >= 0;
              return (
                <tr key={r.crop} className="border-t border-border/60 transition hover:bg-muted/40">
                  <td className="px-3 py-3 font-semibold">{r.crop}</td>
                  <td className="px-3 py-3 text-muted-foreground">{r.market}</td>
                  <td className="px-3 py-3 text-right font-medium">
                    ₹{r.price.toLocaleString()}
                    <span className="ml-1 text-xs text-muted-foreground">/{r.unit}</span>
                  </td>
                  <td className="px-3 py-3">
                    <div
                      className={cn(
                        "ml-auto inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold",
                        up
                          ? "bg-leaf/15 text-leaf"
                          : "bg-destructive/15 text-destructive",
                      )}
                    >
                      {up ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                      {up ? "+" : ""}
                      {r.change}%
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </DashboardCard>
  );
}
