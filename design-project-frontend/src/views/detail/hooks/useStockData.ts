import { ref } from 'vue';
import { request } from '@/service/request';

interface StockDetailData {
  stockCode: string;
  stockName: string;
  latestPrice: string;
  priceChangeRate: string;
  priceChange: string;
  riseSpeed: string;
  ratingOrgNum: number;
  ratingBuyNum: number;
  ratingAddNum: number;
  ratingNeutralNum: number;
  ratingReduceNum: number;
  ratingSaleNum: number;
  year1: number;
  eps1: number;
  year2: number;
  eps2: number;
  year3: number;
  eps3: number;
  year4: number;
  eps4: number;
}

interface RatingData {
  ratingBuyNum: number;
  ratingAddNum: number;
  ratingNeutralNum: number;
  ratingReduceNum: number;
  ratingSaleNum: number;
}

interface StockInfoData {
  stockCode: string;
  summary: string;
  financialDataByYear: Record<string, any>;
}

interface CorrelationData {
  date: string;
  sentimentChange: number;
  priceChange: number;
  correlationSummary: string;
  sentimentCount: number;
}

interface PredictionData {
  modelName: string;
  predictionDate: string;
  predictedPrice: number;
  accuracy: number;
  confidenceLevel: number;
  predictionBasis: string;
}

interface PredictionSummary {
  mostAccurateModel: string;
  oneWeekChange: number;
  oneMonthChange: number;
  threeMonthChange: number;
  modelAccuracy: number;
}

interface UserPortrait {
  content: string;
}

export function useStockData() {
  const stockDetailData = ref<StockDetailData>({} as StockDetailData);
  const stockInfoData = ref<StockInfoData>({} as StockInfoData);
  const ratingData = ref<RatingData>({} as RatingData);
  ratingData.value = {
    ratingBuyNum: stockDetailData.value.ratingBuyNum,
    ratingAddNum: stockDetailData.value.ratingAddNum,
    ratingNeutralNum: stockDetailData.value.ratingNeutralNum,
    ratingReduceNum: stockDetailData.value.ratingReduceNum,
    ratingSaleNum: stockDetailData.value.ratingSaleNum
  };

  const klineData = ref([]);
  const sentimentData = ref([]);
  const wordFreqData = ref([]);
  const correlationData = ref([]);
  const predictionData = ref<PredictionData[]>([]);
  const predictionSummary = ref<PredictionSummary>({} as PredictionSummary);
  const userPortrait = ref<UserPortrait>({} as UserPortrait);

  async function fetchStockFinancialData(stockCode: string) {
    try {
      const result = await request({
        url: '/stock/financial_data',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        params: {
          stockCode
        },
        method: 'GET'
      });
      if (result?.data) {
        stockInfoData.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching financial data:', error);
    }
  }

  async function fetchStockDetailData(stockCode: string) {
    try {
      const result = await request({
        url: '/stock',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        params: {
          stockCode
        },
        method: 'GET'
      });
      if (result?.data) {
        stockDetailData.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching stock detail:', error);
    }
  }

  async function fetchKlineData(stockCode: string) {
    try {
      const result = await request({
        url: '/stock/kline',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        params: {
          stockCode
        },
        method: 'GET'
      });
      if (result) {
        klineData.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching kline data:', error);
    }
  }

  async function fetchSentimentData(stockCode: string) {
    try {
      const result = await request({
        url: '/stock/sentiment',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        params: {
          stockCode
        },
        method: 'GET'
      });
      if (result) {
        sentimentData.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching sentiment data:', error);
    }
  }

  async function fetchWordFrequencyData(stockCode: string) {
    try {
      const result = await request({
        url: '/stock/word-frequency',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        params: {
          stockCode
        },
        method: 'GET'
      });
      if (result) {
        wordFreqData.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching word frequency data:', error);
    }
  }

  async function fetchSentimentCorrelation(stockCode: string) {
    try {
      const result = await request({
        url: '/stock/sentiment-correlation',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        params: {
          stockCode
        },
        method: 'GET'
      });

      if (result?.data) {
        console.log('API Response:', result.data);
        correlationData.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching correlation data:', error);
    }
  }

  async function fetchPredictionData(stockCode: string) {
    try {
      const result = await request({
        url: `/stock/predictions/${stockCode}`,
        method: 'GET'
      });
      if (result?.data) {
        predictionData.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching prediction data:', error);
    }
  }

  async function fetchPredictionSummary(stockCode: string) {
    try {
      const result = await request({
        url: `/stock/predictions/${stockCode}/summary`,
        method: 'GET'
      });
      if (result?.data) {
        predictionSummary.value = result.data;
      }
    } catch (error) {
      console.error('Error fetching prediction summary:', error);
    }
  }

  async function fetchUserPortrait(stockCode: string) {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: "llama3.2",
          messages: [
            {
              role: "user",
              content: `作为一个股票分析专家，请分析股票代码${stockCode}的公司用户画像，包括用户群体特征、消费能力、消费习惯等方面。请给出详细的分析。`
            }
          ],
          stream: false
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();

      if (result?.message?.content) {
        userPortrait.value = {
          content: result.message.content
        };
      }
    } catch (error) {
      console.error('Error fetching user portrait:', error);
      userPortrait.value = {
        content: '抱歉，获取用户画像失败，请稍后重试。'
      };
    }
  }

  return {
    stockDetailData,
    stockInfoData,
    klineData,
    sentimentData,
    wordFreqData,
    correlationData,
    fetchStockFinancialData,
    fetchStockDetailData,
    fetchKlineData,
    fetchSentimentData,
    fetchWordFrequencyData,
    fetchSentimentCorrelation,
    predictionData,
    predictionSummary,
    fetchPredictionData,
    fetchPredictionSummary,
    userPortrait,
    fetchUserPortrait
  };
}
