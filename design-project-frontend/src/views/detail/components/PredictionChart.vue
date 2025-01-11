<template>
  <div>
    <div ref="chartRef" class="prediction-chart"></div>
    <div class="prediction-summary mt-4 p-4 bg-gray-50 rounded">
      <p class="text-lg font-medium">预测总结</p>
      <p v-if="props.summaryData?.mostAccurateModel" class="mt-2">
        在三个模型中，本次预测准确率最高的模型为：{{ props.summaryData.mostAccurateModel }}，
        其预测显示当前股票价格变化趋势为：
      </p>
      <ul class="list-disc list-inside mt-2">
        <li>1周内：<span :class="getChangeClass(props.summaryData?.oneWeekChange)">
          {{ formatPercentageWithSign(props.summaryData?.oneWeekChange) }}
        </span></li>
        <li>1个月内：<span :class="getChangeClass(props.summaryData?.oneMonthChange)">
          {{ formatPercentageWithSign(props.summaryData?.oneMonthChange) }}
        </span></li>
        <li>3个月内：<span :class="getChangeClass(props.summaryData?.threeMonthChange)">
          {{ formatPercentageWithSign(props.summaryData?.threeMonthChange) }}
        </span></li>
      </ul>
      <p class="mt-2">
        本次预测中，该模型的预测准确率为：{{ formatPercentage(props.summaryData?.modelAccuracy) }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import dayjs from 'dayjs';

const props = defineProps({
  predictionData: {
    type: Array,
    required: true
  },
  summaryData: {
    type: Object,
    required: true
  }
});

const chartRef = ref();

const formatPercentage = (value: number) => {
  if (!value && value !== 0) return '--';
  return `${(value * 100).toFixed(2)}%`;
};

const formatPercentageWithSign = (value: number) => {
  if (!value && value !== 0) return '--';
  const sign = value > 0 ? '↑' : value < 0 ? '↓' : '';
  return `${sign}${Math.abs(value * 100).toFixed(2)}%`;
};

const getChangeClass = (value: number) => {
  if (!value && value !== 0) return '';
  return {
    'text-red-500': value > 0,
    'text-green-500': value < 0,
    'text-gray-500': value === 0
  };
};

const initChart = () => {
  if (!chartRef.value || !props.predictionData.length) return;

  const chart = echarts.init(chartRef.value);

  // 按模型分组数据
  const modelGroups = props.predictionData.reduce((acc, curr) => {
    if (!acc[curr.modelName]) {
      acc[curr.modelName] = [];
    }
    acc[curr.modelName].push([
      dayjs(curr.predictionDate).format('YYYY-MM-DD'),
      curr.predictedPrice
    ]);
    return acc;
  }, {});

  const series = Object.entries(modelGroups).map(([modelName, data]) => ({
    name: modelName,
    type: 'line',
    data,
    smooth: true,
    showSymbol: false,
    emphasis: {
      focus: 'series'
    }
  }));

  const option = {
    title: {
      text: '股价趋势预测',
      left: 'center',
      top: 10
    },
    legend: {
      data: Object.keys(modelGroups),
      top: 40,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = dayjs(params[0].data[0]).format('YYYY-MM-DD') + '<br/>';
        params.forEach(param => {
          const modelName = param.seriesName;
          const price = param.data[1].toFixed(2);
          const model = props.predictionData.find(
            p => p.modelName === modelName &&
            dayjs(p.predictionDate).format('YYYY-MM-DD') === param.data[0]
          );
          result += `${modelName}: ${price} (置信度: ${(model?.confidenceLevel * 100).toFixed(2)}%)<br/>`;
        });
        return result;
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '80px',
      containLabel: true
    },
    xAxis: {
      type: 'time',
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      name: '预测股价',
      axisLabel: {
        formatter: '{value}'
      }
    },
    series
  };

  chart.setOption(option);

  window.addEventListener('resize', () => {
    chart.resize();
  });
};

watch(() => props.predictionData, () => {
  initChart();
}, { deep: true });

onMounted(() => {
  initChart();
});
</script>

<style scoped>
.prediction-chart {
  width: 100%;
  height: 400px;
}
</style>
