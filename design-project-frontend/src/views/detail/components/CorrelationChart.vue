<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';

interface CorrelationData {
  date: string;
  sentimentAvg: number;
  nextDayPriceChange: number;
}

interface Props {
  correlationData: CorrelationData[];
}

const props = defineProps<Props>();

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const updateChart = () => {
  if (!props.correlationData?.length) return;

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '情感-股价相关性分析',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['情感值', '次日股价变动'],
      top: '30px'
    },
    xAxis: {
      type: 'category',
      data: props.correlationData.map(item => item.date)
    },
    yAxis: [
      {
        type: 'value',
        name: '情感值',
        position: 'left'
      },
      {
        type: 'value',
        name: '股价变动(%)',
        position: 'right'
      }
    ],
    series: [
      {
        name: '情感值',
        type: 'line',
        data: props.correlationData.map(item => item.sentimentAvg),
        yAxisIndex: 0
      },
      {
        name: '次日股价变动',
        type: 'line',
        data: props.correlationData.map(item => item.nextDayPriceChange),
        yAxisIndex: 1
      }
    ]
  };

  chartInstance?.setOption(option);
};

watch(() => props.correlationData, updateChart, { deep: true });

onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    if (props.correlationData?.length) {
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
  <div ref="chartRef" class="chart-container"></div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
}
</style>
