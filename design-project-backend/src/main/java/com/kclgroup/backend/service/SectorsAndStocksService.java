package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.SectorsAndStocks;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;

/**
* @author 张小明
* @description 针对表【sectors_and_stocks】的数据库操作Service
* @createDate 2024-06-24 20:57:12
*/
public interface SectorsAndStocksService extends IService<SectorsAndStocks> {
    List<SectorsAndStocks> getSectorsAndStocks();
}
