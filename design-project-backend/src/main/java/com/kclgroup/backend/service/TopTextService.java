package com.kclgroup.backend.service;

import com.kclgroup.backend.mapper.TopTextMapper;
import com.kclgroup.backend.pojo.entity.TopText;
import com.baomidou.mybatisplus.extension.service.IService;
import org.springframework.beans.factory.annotation.Autowired;

/**
* @author 张小明
* @description 针对表【top_text】的数据库操作Service
* @createDate 2024-06-24 15:22:14
*/
public interface TopTextService extends IService<TopText> {
    public TopText getTopText();
}
