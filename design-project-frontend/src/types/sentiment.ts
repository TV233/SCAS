export interface SentimentPriceCorrelation {
  stockCode: string;
  date: string;
  sentimentAvg: number;
  priceChange: number;
  nextDayPriceChange: number;
  correlation: number;
  sentimentCount: number;
  isSignificant: number;
  updateTime: string;
}
