<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';

interface KlineData {
  dateTime: string;
  openPrice: number;
  closePrice: number;
  lowPrice: number;
  highPrice: number;
}

interface SentimentData {
  date: string;
  sentimentAvg: number;
  commentCount: number;
}

interface Props {
  klineData: KlineData[];
  sentimentData: SentimentData[];
}

const props = defineProps<Props>();

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const updateChart = () => {
  if (!props.klineData?.length) return;

  const klineOption = {
    backgroundColor: 'transparent',
    title: {
      text: props.sentimentData?.length ? 'K线图与评论情感趋势' : 'K线图',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: function (params) {
        const date = params[0].axisValue;
        let res = `${date}<br/>`;
        params.forEach(param => {
          if (param.seriesName === 'K线') {
            res += `${param.seriesName}: 开盘${param.data[1]}, 收盘${param.data[2]}, 最低${param.data[3]}, 最高${param.data[4]}<br/>`;
          } else {
            res += `${param.seriesName}: ${param.data}<br/>`;
          }
        });
        return res;
      }
    },
    legend: {
      data: props.sentimentData?.length ? ['K线', '情感值', '评论数'] : ['K线'],
      top: '30px'
    },
    grid: {
      left: '10%',
      right: props.sentimentData?.length ? '10%' : '5%',
      bottom: '15%'
    },
    xAxis: {
      type: 'category',
      data: props.klineData.map(item => item.dateTime),
      scale: true,
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax'
    },
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true
        }
      },
      ...(props.sentimentData?.length ? [
        {
          scale: true,
          name: '情感值',
          min: 0,
          max: 1,
          position: 'right',
          offset: 80,
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ff7f0e'
            }
          },
          axisLabel: {
            formatter: '{value}'
          }
        },
        {
          scale: true,
          name: '评论数',
          position: 'right',
          offset: 160,
          axisLine: {
            show: true,
            lineStyle: {
              color: '#2ca02c'
            }
          },
          axisLabel: {
            formatter: '{value}'
          }
        }
      ] : [])
    ],
    dataZoom: [
      {
        type: 'inside',
        start: 50,
        end: 100
      },
      {
        show: true,
        type: 'slider',
        bottom: '3%',
        start: 50,
        end: 100
      }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: props.klineData.map(item => [
          item.openPrice,
          item.closePrice,
          item.lowPrice,
          item.highPrice
        ]),
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        }
      }
    ]
  };

  // 添加情感数据系列
  if (props.sentimentData?.length) {
    const dateMap = new Map();
    props.sentimentData.forEach(item => {
      dateMap.set(item.date, item);
    });

    const alignedSentimentData = props.klineData.map(kline => {
      const sentiment = dateMap.get(kline.dateTime);
      return sentiment ? sentiment.sentimentAvg : null;
    });

    const alignedCommentData = props.klineData.map(kline => {
      const sentiment = dateMap.get(kline.dateTime);
      return sentiment ? sentiment.commentCount : null;
    });

    klineOption.series.push(
      {
        name: '情感值',
        type: 'line',
        yAxisIndex: 1,
        data: alignedSentimentData,
        smooth: true,
        lineStyle: {
          width: 2
        },
        itemStyle: {
          color: '#ff7f0e'
        }
      },
      {
        name: '评论数',
        type: 'bar',
        yAxisIndex: 2,
        data: alignedCommentData,
        itemStyle: {
          color: '#2ca02c'
        }
      }
    );
  }

  chartInstance?.setOption(klineOption);
};

watch([() => props.klineData, () => props.sentimentData], updateChart, { deep: true });

onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    if (props.klineData?.length) {
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
