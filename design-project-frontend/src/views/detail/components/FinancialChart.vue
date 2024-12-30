<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';

interface FinancialData {
  totalOperatereveIncrease: number;
  parentNetprofitIncrease: number;
  dnetprofitatpcTcalIncrease: number;
}

interface Props {
  stockInfoData: {
    financialDataByYear: Record<string, FinancialData>;
  };
}

const props = defineProps<Props>();

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const updateChart = () => {
  if (!props.stockInfoData?.financialDataByYear) return;

  const config = {
    backgroundColor: 'transparent',
    title: {
      text: '股票年报数据',
      left: 'center',
      top: '2%'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['营业总收入', '归母净利润', '扣非归母净利润'],
      top: '8%'
    },
    xAxis: {
      type: 'category',
      data: Object.keys(props.stockInfoData.financialDataByYear),
      name: ' ',
      nameLocation: 'middle',
      nameGap: 25
    },
    yAxis: [
      {
        type: 'value',
        name: '营业总收入',
        nameLocation: 'middle',
        nameGap: 40,
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: '归母净利润/扣非归母净利润',
        nameLocation: 'middle',
        nameGap: 60,
        axisLabel: {
          formatter: '{value}'
        }
      }
    ],
    series: [
      {
        name: '营业总收入',
        type: 'line',
        yAxisIndex: 0,
        data: Object.values(props.stockInfoData.financialDataByYear).map(
          yearData => yearData.totalOperatereveIncrease
        ),
        itemStyle: {
          color: '#ff0000'
        }
      },
      {
        name: '归母净利润',
        type: 'line',
        yAxisIndex: 1,
        data: Object.values(props.stockInfoData.financialDataByYear).map(
          yearData => yearData.parentNetprofitIncrease
        ),
        itemStyle: {
          color: '#00ff00'
        }
      },
      {
        name: '扣非归母净利润',
        type: 'line',
        yAxisIndex: 1,
        data: Object.values(props.stockInfoData.financialDataByYear).map(
          yearData => yearData.dnetprofitatpcTcalIncrease
        ),
        itemStyle: {
          color: '#0000ff'
        }
      }
    ],
    animationEasing: 'linear',
    animationDuration: 2000
  };

  chartInstance?.setOption(config);
};

watch(() => props.stockInfoData, updateChart, { deep: true });

onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    if (props.stockInfoData?.financialDataByYear) {
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
  height: 20rem;
}
</style>
