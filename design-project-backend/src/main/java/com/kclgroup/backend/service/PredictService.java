package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.Predict;
import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.vo.PredictVo;

import java.math.BigDecimal;
import java.util.List;

/**
* @author 张小明
* @description 针对表【predict】的数据库操作Service
* @createDate 2024-06-24 21:18:07
*/
public interface PredictService extends IService<Predict> {

    List<PredictVo> getPredict();

    Integer getRatingOrgNum(String stockCode);

    BigDecimal getRatingBuyNum(String stockCode);

    BigDecimal getRatingAddNum(String stockCode);

    BigDecimal getRatingSaleNum(String stockCode);

    BigDecimal getRatingNeutralNum(String stockCode);

    BigDecimal getRatingReduceNum(String stockCode);

    Integer getYear1(String stockCode);

    BigDecimal getEps1(String stockCode);

    Integer getYear2(String stockCode);

    BigDecimal getEps2(String stockCode);

    Integer getYear3(String stockCode);

    BigDecimal getEps3(String stockCode);

    Integer getYear4(String stockCode);

    BigDecimal getEps4(String stockCode);
}
