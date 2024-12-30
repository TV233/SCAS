<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';

interface Props {
  stockDetailData: {
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
    title: {
      text: '股票收益预测',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: [
        props.stockDetailData.year1,
        props.stockDetailData.year2,
        props.stockDetailData.year3,
        props.stockDetailData.year4
      ],
      name: ' ',
      nameLocation: 'middle',
      nameGap: 25
    },
    yAxis: {
      type: 'value',
      name: '每股收益 (EPS)',
      nameLocation: 'middle',
      nameGap: 40
    },
    series: [
      {
        data: [
          props.stockDetailData.eps1,
          props.stockDetailData.eps2,
          props.stockDetailData.eps3,
          props.stockDetailData.eps4
        ],
        type: 'bar',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#ff7f0e' },
            { offset: 0.5, color: '#ff5722' },
            { offset: 1, color: '#e64a19' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#ff5722' },
              { offset: 0.7, color: '#e64a19' },
              { offset: 1, color: '#d84315' }
            ])
          }
        },
        animationDelay: idx => idx * 200
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
  <div ref="chartRef" class="chart-container"></div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 18rem;
}
</style>
