<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';

interface Props {
  stockDetailData: {
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
  };
}

const props = defineProps<Props>();

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const updateChart = () => {
  if (!props.stockDetailData) return;

  const config = {
    backgroundColor: 'transparent',
    series: [
      {
        type: 'pie',
        radius: '40%',
        data: [
          { value: props.stockDetailData.ratingBuyNum || 0, name: '买入', itemStyle: { color: '#d62728' } },
          { value: props.stockDetailData.ratingAddNum || 0, name: '增持', itemStyle: { color: '#ff7f0e' } },
          { value: props.stockDetailData.ratingNeutralNum || 0, name: '观望', itemStyle: { color: '#2ca02c' } },
          { value: props.stockDetailData.ratingReduceNum || 0, name: '减持', itemStyle: { color: '#9467bd' } },
          { value: props.stockDetailData.ratingSaleNum || 0, name: '卖出', itemStyle: { color: '#1f77b4' } }
        ].filter(item => item.value > 0),
        label: {
          fontSize: 10,
          formatter(params) {
            return `${params.name}: ${params.value}`;
          }
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  chartInstance?.setOption(config);
};

watch(() => props.stockDetailData, updateChart, { deep: true });

onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    if (props.stockDetailData) {
      updateChart();
    }
  }
});

onUnmounted(() => {
  chartInstance?.dispose();
});

const handleResize = () => {
  chartInstance?.resize();
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<template>
  <div>
    <div class="mb-2 mt-5 w-full flex-x-center text-5 font-bold">
      近期证券机构研报评级分布
      <icon-tdesign:compass class="ml-1 mt-2" />
    </div>
    <div ref="chartRef" class="chart-container mb--17 mt--14 flex-x-center"></div>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 15rem;
}
</style>
