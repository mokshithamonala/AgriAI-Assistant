export const languages = ["English", "Hindi", "Malayalam","Tamil", "Kannada"] as const;

export const marketPrices = [
  { crop: "Rice", market: "Bengaluru APMC", price: 2850, unit: "quintal", change: 2.4 },
  { crop: "Wheat", market: "Indore Mandi", price: 2410, unit: "quintal", change: -1.1 },
  { crop: "Cotton", market: "Guntur", price: 7280, unit: "quintal", change: 3.6 },
  { crop: "Tomato", market: "Kolar", price: 32, unit: "kg", change: -4.2 },
  { crop: "Onion", market: "Lasalgaon", price: 28, unit: "kg", change: 1.8 },
  { crop: "Maize", market: "Davangere", price: 2180, unit: "quintal", change: 0.6 },
];

export const schemes = [
  {
    name: "PM-KISAN",
    tag: "Direct Income Support",
    description:
      "₹6,000 per year direct benefit transfer to eligible small and marginal farmer families.",
  },
  {
    name: "Soil Health Card",
    tag: "Soil Advisory",
    description:
      "Personalised soil nutrient reports and crop-wise fertilizer recommendations every 3 years.",
  },
  {
    name: "PMFBY",
    tag: "Crop Insurance",
    description:
      "Comprehensive crop insurance against yield loss due to non-preventable natural risks.",
  },
  {
    name: "Kisan Credit Card",
    tag: "Affordable Credit",
    description:
      "Short-term credit at concessional rates for cultivation, post-harvest and household needs.",
  },
];

export const weather = {
  location: "Mysuru, Karnataka",
  temperature: 28,
  condition: "Partly Cloudy",
  humidity: 68,
  rainfall: 12,
  wind: 14,
  forecast: [
    { day: "Mon", t: 29, c: "sun" },
    { day: "Tue", t: 27, c: "cloud" },
    { day: "Wed", t: 26, c: "rain" },
    { day: "Thu", t: 28, c: "sun" },
    { day: "Fri", t: 30, c: "sun" },
  ],
};

export const stats = [
  { label: "Active Crops", value: "4", hint: "+1 this season" },
  { label: "Soil Health", value: "82%", hint: "Good condition" },
  { label: "Water Usage", value: "1.2k L", hint: "-8% vs last week" },
  { label: "Advisory Alerts", value: "3", hint: "2 new today" },
];
