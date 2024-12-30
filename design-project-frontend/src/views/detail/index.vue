<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { request } from '@/service/request';
import 'echarts-wordcloud';
import StockBasicInfo from './components/StockBasicInfo.vue';
import { useStockData } from './hooks/useStockData';
import RatingChart from './components/RatingChart.vue';
import EpsChart from './components/EpsChart.vue';
import KlineChart from './components/KlineChart.vue';
import FinancialChart from './components/FinancialChart.vue';
import WordCloudChart from './components/WordCloudChart.vue';
import CorrelationChart from './components/CorrelationChart.vue';
const route = useRoute();
const router = useRouter();

const stockCode = route.query.stockCode as string;

const {
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
  fetchSentimentCorrelation
} = useStockData();

const goBack = () => {
  router.back();
};

const onAdd = async code => {
  try {
    const response = await request({
      url: '/favor',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: {
        stockCode: code
      }
    });

    if (response) {
      alert('添加成功');
    } else {
      alert('已在自选股中');
    }
  } catch (error) {
    // alert('已在自选股中');
  }
};

// 数据加载逻辑
onMounted(async () => {
  if (stockCode) {
    await Promise.all([
      fetchStockFinancialData(stockCode),
      fetchStockDetailData(stockCode),
      fetchKlineData(stockCode),
      fetchSentimentData(stockCode),
      fetchWordFrequencyData(stockCode),
      fetchSentimentCorrelation(stockCode)
    ]);
  }
});
</script>

<template>
  <div>
    <ATooltip placement="right">
      <template #title>返回</template>
      <AButton shape="circle" @click="goBack"><icon-ic:outline-keyboard-arrow-left class="h-8 w-8 pb-2" /></AButton>
    </ATooltip>
    <ARow class="flex justify-between">
      <ACard :bordered="false" class="mt-2 w-35% card-wrapper">
        <StockBasicInfo
          :stock-detail-data="stockDetailData"
          :stock-info-data="stockInfoData"
          :stock-code="stockCode"
          @add="onAdd"
        />
        <RatingChart :stock-detail-data="stockDetailData" />
      </ACard>
      <ACard :bordered="false" class="mt-2 w-60% card-wrapper">
        <EpsChart :stock-detail-data="stockDetailData" />
      </ACard>
    </ARow>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <KlineChart
        :kline-data="klineData"
        :sentiment-data="sentimentData"
      />
    </ACard>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <CorrelationChart :correlation-data="correlationData" />
    </ACard>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <FinancialChart :stock-info-data="stockInfoData" />
    </ACard>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <WordCloudChart :word-freq-data="wordFreqData" />
    </ACard>
  </div>
</template>

<style scoped>
.sentiment-chart-container,
.wordcloud-chart-container {
  width: 100%;
  height: 400px;
}
</style>
