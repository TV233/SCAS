package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.EmotionIndex;
import com.baomidou.mybatisplus.extension.service.IService;

/**
* @author 张小明
* @description 针对表【emotion_index】的数据库操作Service
* @createDate 2024-06-24 20:48:29
*/
public interface EmotionIndexService extends IService<EmotionIndex> {

    EmotionIndex getEmotionIndex();
}
