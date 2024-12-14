package com.kclgroup.backend.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.entity.StockKline;
import com.kclgroup.backend.pojo.vo.KlineVo;

import java.util.List;

public interface StockKlineService extends IService<StockKline> {
    List<KlineVo> getStockKline(String stockCode);
}
