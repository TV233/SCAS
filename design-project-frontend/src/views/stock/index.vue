<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { request } from '@/service/request';
import { useRouterPush } from '@/hooks/common/router';
const { routerPushByKey } = useRouterPush();
const favorData = ref([]);

// 从后端获取市场风向数据
async function fetchFavor() {
  try {
    const result = await request({
      url: '/favor/getList',
      method: 'GET'
    });
    if (result) {
      // 映射数据以符合表格结构
      console.log(result.data);
      favorData.value = result.data.map((item, index) => ({
        key: index,
        name: item.stockName,
        code: item.stockCode,
        price: item.latestPrice.toFixed(2),
        change: item.priceChange.toFixed(2),
        rate: item.priceChangeRate.toFixed(2)
      }));
    } else {
      // console.error('Error fetching data:', result.message);
    }
  } catch (error) {
    // console.error('Error fetching data:', error);
  }
}

onMounted(() => {
  fetchFavor();
});
const columns = [
  { title: '股票名称', dataIndex: 'name', key: 'name', fixed: 'left', width: 150 },
  { title: '股票代码', dataIndex: 'code', key: 'code', width: 120 },
  { title: '当前股价', dataIndex: 'price', key: 'price', width: 100 },
  { title: '股票涨幅', dataIndex: 'change', key: 'change', width: 100, slots: { customRender: 'change' } },
  { title: '增长率', dataIndex: 'rate', key: 'rate', width: 100, slots: { customRender: 'rate' } },
  { title: '操作', key: 'action', fixed: 'right', width: 100, slots: { customRender: 'action' } }
];

const handleAction = record => {
  routerPushByKey('detail', { query: { stockCode: record.code } });
};

const onDelete = async code => {
  try {
    const response = await request({
      url: '/favor/cancel',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: {
        stockCode: code
      }
    });
    if (response) {
      favorData.value = favorData.value.filter(item => item.code !== code);
      alert('删除成功');
    } else {
      alert('删除失败，请联系管理员');
    }
  } catch (error) {
    alert('删除失败，请联系管理员');
  }
};
</script>

<template>
  <ACard>
    <div class="mb-3 text-7 font-bold">我的自选股</div>
    <ATable :columns="columns" :data-source="favorData" :scroll="{ x: '100%' }" :pagination="false">
      <template #change="{ record }">
        <span :style="{ color: record.change < 0 ? '#3f8600' : '#cf1322', fontSize: '16px' }">
          {{ record.change }}
        </span>
      </template>
      <template #rate="{ record }">
        <span :style="{ color: record.rate < 0 ? '#3f8600' : '#cf1322', fontSize: '16px' }">{{ record.rate }}%</span>
      </template>
      <template #action="{ record }">
        <div style="display: flex; align-items: center; gap: 8px">
          <!-- 查看详情按钮，设置为橙色 -->
          <AButton
            type="primary"
            style="background-color: orange; border-color: orange; color: white"
            @click="() => handleAction(record)"
          >
            查看详情
          </AButton>
          <!-- 删除按钮，设置为红色并字体为白色 -->
          <APopconfirm title="确定要删除这个项目吗？" @confirm="() => onDelete(record.code)">
            <AButton type="danger" style="background-color: red; border-color: red; color: white">删除</AButton>
          </APopconfirm>
        </div>
      </template>
    </ATable>
  </ACard>
</template>
