<script setup lang="ts">
import { ref } from 'vue';
import { request } from '@/service/request';

// 初始默认值
const userInfo = ref({
  id: 0,
  username: '默认用户名',
  nickname: '默认昵称',
  email: '默认邮箱',
  createTime: '默认创建时间',
  updateTime: '默认更新时间'
});

const model = ref({
  old_pwd: '',
  new_pwd: '',
  re_pwd: ''
});

const rules = {
  old_pwd: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_pwd: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
  re_pwd: [{ required: true, message: '请确认新密码', trigger: 'blur' }]
};

const formRef = ref(null);
const visible = ref(false);

const getUserInfo = async () => {
  try {
    const response = await request({
      url: '/user/userInfo',
      method: 'GET'
    });
    if (response) {
      userInfo.value = response.data;
    } else {
      // console.error('获取用户信息失败:', response.message);
    }
  } catch (error) {
    // console.error('获取用户信息失败:', error);
  }
};

const updateUserInfo = async () => {
  try {
    const response = await request({
      url: '/user/update',
      method: 'PUT',
      data: {
        id: userInfo.value.id,
        nickname: userInfo.value.nickname,
        email: userInfo.value.email
      }
    });
    if (response) {
      alert('用户信息更新成功');
    } else {
      // alert('用户信息更新失败:'+ response.message);
    }
  } catch (error) {
    // alert('用户信息更新失败:'+ error);
  }
};

const updateUserPassword = async () => {
  if (userInfo.value.password !== userInfo.value.password2) {
    alert('两次密码输入不一致');
    return;
  }
  try {
    const response = await request({
      url: '/user/updatePwd',
      method: 'PATCH',
      data: {
        old_pwd: model.value.old_pwd,
        new_pwd: model.value.new_pwd,
        re_pwd: model.value.re_pwd
      }
    });
    if (response) {
      alert('密码更新成功');
      visible.value = false;
      window.location.reload();
    } else {
      alert('密码更新失败:'+ response.message);
    }
  } catch (error) {
    // alert('密码更新失败:'+ response.message);
  }
};

const handleSubmit = () => {
  formRef.value
    .validate()
    .then(() => {
      updateUserPassword();
    })
    .catch(error => {
      console.log('验证失败', error);
    });
};

const showModal = () => {
  visible.value = true;
};

const handleOk = () => {
  handleSubmit();
};

const handleCancel = () => {
  visible.value = false;
};

const handleChange = () => {
  updateUserInfo();
};

// 示例调用
getUserInfo();
</script>

<template>
  <div>
    <!-- 用户信息 -->
    <ADescriptions title="用户信息" bordered>
      <ADescriptionsItem label="ID">
        <AInput v-model:value="userInfo.id" readonly />
      </ADescriptionsItem>
      <ADescriptionsItem label="用户名">
        <AInput v-model:value="userInfo.username" readonly />
      </ADescriptionsItem>
      <ADescriptionsItem label="昵称">
        <AInput v-model:value="userInfo.nickname" />
      </ADescriptionsItem>
      <ADescriptionsItem label="邮箱">
        <AInput v-model:value="userInfo.email" />
      </ADescriptionsItem>
      <ADescriptionsItem label="创建时间">
        <AInput v-model:value="userInfo.createTime" readonly />
      </ADescriptionsItem>
      <ADescriptionsItem label="更新时间">
        <AInput v-model:value="userInfo.updateTime" readonly />
      </ADescriptionsItem>
    </ADescriptions>
    <AButton type="primary" class="mt-4" @click="handleChange">提交信息更改</AButton>
    <!-- 重置密码按钮 -->
    <AButton type="primary" class="mt-4" @click="showModal">修改密码</AButton>

    <!-- 重置密码模态框 -->
    <AModal v-model:visible="visible" title="重置密码" @ok="handleOk" @cancel="handleCancel">
      <AForm ref="formRef" :model="model" :rules="rules">
        <AFormItem name="old_pwd" label="旧密码">
          <AInputPassword v-model:value="model.old_pwd" size="large" placeholder="请输入旧密码" />
        </AFormItem>
        <AFormItem name="new_pwd" label="新密码">
          <AInputPassword v-model:value="model.new_pwd" size="large" placeholder="请输入新密码" />
        </AFormItem>
        <AFormItem name="re_pwd" label="确认新密码">
          <AInputPassword v-model:value="model.re_pwd" size="large" placeholder="请确认新密码" />
        </AFormItem>
      </AForm>
    </AModal>
  </div>
</template>

<style scoped>
/* 你的样式代码 */
</style>
