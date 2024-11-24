<script setup lang="ts">
import { computed ,onMounted,ref } from 'vue';
import { request } from '@/service/request';

defineOptions({ name: 'MarketBlock' });
const marketData = ref([]);
// 从后端获取市场风向数据
async function fetchMarketStyle() {
  try {
    const result = await request({
      url: '/api/market_style',
      method: 'GET'
    });
    if (result) {
      marketData.value = result.data;  // 存储获取到的股票指数数据
    } else {
      // console.error('Error fetching stock indices:', result.message);
    }
  } catch (error) {
    // console.error('Error fetching stock indices:', error);
  }
}

onMounted(() => {
  fetchMarketStyle(); // 组件挂载时调用函数获取数据
});
const blockData = computed<any>(() => [
  { name: '水泥', changeRate: 1.81, topName: '供给侧改革' },
  { name: '钢铁', changeRate: 2.11, topName: '供给侧改革' },
  { name: '国企改革', changeRate: 2.22, topName: '专题' },
  { name: '券商', changeRate: 1.56, topName: '' },
  { name: '房地产', changeRate: 0.96, topName: '供给侧改革' },
  { name: '银行', changeRate: 0.5, topName: '' },
  { name: '上证50', changeRate: 0.43, topName: '' },
  { name: '影视娱乐', changeRate: 3.77, topName: '大消费' },
  { name: '白酒', changeRate: 1.53, topName: '大消费' },
  { name: '低市盈率', changeRate: 0.92, topName: '' },
  { name: '白马股', changeRate: 2.12, topName: '' },
  { name: '大消费', changeRate: 1.94, topName: '专题' },
  { name: '医药', changeRate: 1.92, topName: '大消费' },
  { name: '行业龙头', changeRate: 1.09, topName: '' },
  { name: '数字阅读', changeRate: 6.6, topName: '' },
  { name: '短剧互动游戏', changeRate: 6.49, topName: '' },
  { name: 'Web3.0', changeRate: 7.8, topName: '' },
  { name: '知识产权', changeRate: 6.73, topName: '' },
  { name: 'Sora概念(文生视频)', changeRate: 9.33, topName: '' },
  { name: '智慧医疗', changeRate: 4.6, topName: '人工智能' },
  { name: '人脑工程', changeRate: 4.84, topName: '' },
  { name: '医药', changeRate: 1.92, topName: '大消费' },
  { name: '军工', changeRate: 3, topName: '专题' },
  { name: '银行', changeRate: 0.5, topName: '' },
  { name: '黄金', changeRate: 1.09, topName: '金属' },
  { name: '水泥', changeRate: 1.81, topName: '供给侧改革' },
  { name: '钢铁', changeRate: 2.11, topName: '供给侧改革' },
  { name: '化工', changeRate: 2.54, topName: '' },
  { name: '煤炭', changeRate: 0.96, topName: '供给侧改革' },
  { name: '有色金属', changeRate: 2.09, topName: '供给侧改革' }
]);
</script>

<template>
  <ACard class="mt-3 flex p-x-2 p-y-1">
    <div class="text-5 font-bold w-full mb-2">
      <icon-svg-spinners:blocks-shuffle-3 />
      市场风向
    </div>
    <ACardGrid
      v-for="item in marketData"
      :key="item.name"
      style="width: 23.5%; text-align: center; border: 2px solid #fae7e7"
      class="m-1 !rounded-md h-17 cursor-pointer"
    >
      <div class="mt--5">
        <div class="overflow-hidden text-ellipsis whitespace-nowrap text-3.5 font-bold">
          {{ item.name }}
        </div>
        <!-- 使用computed style动态切换涨跌颜色 -->
        <CountTo
          suffix="%"
          :decimals="2"
          :start-value="0"
          :end-value="item.changeRate"
          :class="`text-3.5 font-bold ${item.changeRate >= 0 ? 'text-[#fe2435]' : 'text-[#08aa4b]'}`"
        />
        <div class="text-3 mt--1">{{ item.topName }}</div>
      </div>
    </ACardGrid>
  </ACard>
</template>


<style scoped></style>
