<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRouterPush } from '@/hooks/common/router';
import { request } from '@/service/request';
defineOptions({ name: 'BestRank' });
const { routerPushByKey } = useRouterPush();

const ranksData = ref([]);
// 从后端获取市场风向数据
async function fetchPredict() {
  try {
    const result = await request({
      url: '/api/predict',
      method: 'GET'
    });
    if (result) {
      // 添加排名到数据
      ranksData.value = result.data.map((item, index) => ({
        id: index + 1, // 动态生成排名
        ...item
      }));
    } else {
      // console.error('Error fetching stock indices:', result.message);
    }
  } catch (error) {
    // console.error('Error fetching stock indices:', error);
  }
}
onMounted(() => {
  fetchPredict(); // 组件挂载时调用函数获取数据
});

const columns = [
  { title: '预测收益排名', dataIndex: 'id' },
  { title: '股票名称', dataIndex: 'stockName' },
  { title: '股票代码', dataIndex: 'stockCode' },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    slots: { customRender: 'action' }
  }
];

const data = [
  {
    stockCode: '600519',
    stockName: '贵州茅台'
  }
  // 其他数据项...
];

const rankData = data.map((item, index) => ({
  id: index + 1,
  ...item
}));

const handleAction = (record: any) => {
  const stockCode = record.stockCode;
  routerPushByKey('detail', { query: { stockCode } });
};
</script>

<template>
  <Simplebar>
    <ATable
      :pagination="false"
      :scroll="{ y: 730 }"
      class="ant-table-striped"
      size="middle"
      :columns="columns"
      :data-source="ranksData"
    >
      <template #action="{ record }">
        <a @click="() => handleAction(record)">
          <ATooltip placement="bottom">
            <template #title>查看详情</template>
            <AButton shape="circle" class="mt-2 h-8 w-4">
              <icon-material-symbols:arrow-forward-ios class="h-5 w-5" />
            </AButton>
          </ATooltip>
        </a>
      </template>
    </ATable>
  </Simplebar>
</template>

<style scoped></style>
