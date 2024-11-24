package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.IndexKlines;
import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.vo.IndexKlineVo;

import java.util.List;

/**
* @author 张小明
* @description 针对表【index_klines】的数据库操作Service
* @createDate 2024-07-02 13:08:39
*/
public interface IndexKlinesService extends IService<IndexKlines> {


    List<IndexKlineVo> getIndexKlines(String indexCode);
}
