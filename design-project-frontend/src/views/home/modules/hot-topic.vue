<script setup lang="ts">
import { computed, ref,onMounted } from 'vue';
import type { CarouselProps } from 'ant-design-vue';
import { useRouterPush } from '@/hooks/common/router';
import { request } from '@/service/request';
const { routerPushByKey } = useRouterPush();
defineOptions({
  name: 'HotTopic'
});
const hotTopicData = ref([]);
async function fetchHotTopic() {
  try {
    const result = await request({
      url: '/api/sectors',
      method: 'GET'
    });
    if (result) {
      hotTopicData.value = result.data;  // 存储获取到的股票指数数据
    } else {
      console.error('Error fetching stock indices:', result.message);
    }
  } catch (error) {
    console.error('Error fetching stock indices:', error);
  }
}

const hotTopic = computed<any>(() => [
  {
    sector: 'Sora概念(文生视频)',
    reason: '“国产Sora”落地提速 Al改写视频产业链',
    stockCode: '300578',
    stockName: '会畅通讯'
  },
  {
    sector: 'Sora概念(文生视频)',
    reason: '“国产Sora”落地提速 Al改写视频产业链',
    stockCode: '300781',
    stockName: '因赛集团'
  },
  {
    sector: '减肥药',
    reason: '超级赛道重大官宣！中国减肥药市场巨大',
    stockCode: '605116',
    stockName: '奥锐特'
  },
  {
    sector: '减肥药',
    reason: '超级赛道重大官宣！中国减肥药市场巨大',
    stockCode: '688117',
    stockName: '圣诺生物'
  }
]);
const dotPosition = ref<CarouselProps['dotPosition']>('right');
  onMounted(() => {
    fetchHotTopic(); 
});
</script>

<template>
  <ACard :bordered="false" class="h-28 w-100% card-wrapper">
    <ACarousel :dot-position="dotPosition" autoplay :dots="false" class="h-10%">
      <div v-for="item in hotTopicData" :key="item.sector">
        <ACard :bordered="false" class="mb--5 mt--6 h-100%">
          <div class="flex justify-between">
            <div class="text-5 font-bold">
              <icon-emojione:fire />
              热门话题: {{ item.sector }}
            </div>
            <div class="w-34 border-2 border-[#fe2435] text-center align-middle text-4 font-bold">
              {{ item.stockName }} {{ item.stockCode }}
            </div>
          </div>
          <div class="flex justify-between">
            <div class="mt-2 text-4">{{ item.reason }}</div>
            <ATooltip placement="left">
              <template #title>查看详情</template>
              <AButton
                shape="circle"
                class="mt-2"
                @click="routerPushByKey('detail', { query: { stockCode: item.stockCode } })"
              >
                <icon-material-symbols:arrow-forward-ios class="h-6 w-6 text-40" />
              </AButton>
            </ATooltip>
          </div>
        </ACard>
      </div>
    </ACarousel>
  </ACard>
</template>

<style scoped>
/* For demo */
:deep(.slick-slide) {
  height: 0rem;
  overflow: hidden;
}

:deep(.slick-slide h3) {
  color: #000;
}
</style>
