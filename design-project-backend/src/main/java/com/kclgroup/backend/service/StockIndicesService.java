package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.StockIndices;
import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.vo.StockIndicesVo;

import java.util.List;

/**
* @author 张小明
* @description 针对表【stock_indices】的数据库操作Service
* @createDate 2024-07-01 21:31:24
*/
public interface StockIndicesService extends IService<StockIndices> {

    List<StockIndicesVo> getStockIndices();
}
